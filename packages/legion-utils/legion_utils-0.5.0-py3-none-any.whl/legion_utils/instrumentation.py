from abc import abstractmethod, ABC
from functools import wraps
from itertools import count
from pathlib import Path
from random import randint
from threading import Event, Thread
from time import sleep
from traceback import format_exc
from typing import Callable, Union, Optional, Dict, Any, List

from loguru import logger as log
from robotnikmq import RobotnikConfig

from legion_utils import WarningMsg, ErrorMsg, CriticalMsg, broadcast_alert_msg
from legion_utils.core import hostname
from legion_utils.princeps.princeps import ServiceRegistrar, TimeDelta, DEFAULT_SERVICE_REGISTRY_DIR

DEFAULT_RELAUNCH_DELAY = 5  # how many seconds to wait before relaunching a given service
DEFAULT_START_DELAY_MAX = 5  # by default, start delay is randomized between 0 and this number of seconds
DEFAULT_CHECKIN_DELAY = 30  # the delay between when the application checks in
DEFAULT_CHECKIN_INTERVAL = DEFAULT_CHECKIN_DELAY * 2  # the time limit for princeps to expect another check-in
DEFAULT_TTL = DEFAULT_CHECKIN_INTERVAL * 2  # the time limit for an alert to live based on missed checkins


class Alerter(ABC):
    def __init__(self,
                 task_id: str,
                 exchange: str,
                 route: str,
                 default_ttl: int,
                 config: Optional[RobotnikConfig] = None):
        self.task_id = task_id
        self.exchange = exchange
        self.route = route
        self.config = config
        self.default_ttl = default_ttl

    @abstractmethod
    def key(self, task_id: str) -> List[str]:
        pass  # pragma: no cover

    def broadcast_warning(self, contents: Dict[str, Any],
                          desc: str,
                          ttl: Optional[int] = None) -> None:
        broadcast_alert_msg(exchange=self.exchange,
                            route=self.route,
                            config=self.config,
                            alert=WarningMsg(contents=contents,
                                             key=self.key(self.task_id),
                                             desc=desc,
                                             ttl=(ttl or self.default_ttl)))

    def broadcast_error(self, contents: Dict[str, Any],
                        desc: str,
                        ttl: Optional[int] = None) -> None:
        broadcast_alert_msg(exchange=self.exchange,
                            route=self.route,
                            config=self.config,
                            alert=ErrorMsg(contents=contents,
                                           key=self.key(self.task_id),
                                           desc=desc,
                                           ttl=(ttl or self.default_ttl)))

    def broadcast_critical(self, contents: Dict[str, Any],
                           desc: str,
                           ttl: Optional[int] = None) -> None:
        broadcast_alert_msg(exchange=self.exchange,
                            route=self.route,
                            config=self.config,
                            alert=CriticalMsg(contents=contents,
                                              key=self.key(self.task_id),
                                              desc=desc,
                                              ttl=(ttl or self.default_ttl)))


class Runner(Alerter):
    def __init__(self,
                 task_id: str,
                 exchange: str,
                 route: str,
                 default_ttl: int,
                 start_delay: Union[int, Callable[[], int], None],
                 halt_flag: Optional[Event],
                 service_registry_dir: Optional[Path],
                 check_in_delay: int,
                 warn_after_checkin: Optional[TimeDelta],
                 error_after_checkin: Optional[TimeDelta],
                 critical_after_checkin: Optional[TimeDelta],
                 config: Optional[RobotnikConfig] = None):
        super().__init__(task_id=task_id, exchange=exchange, route=route, default_ttl=default_ttl, config=config)
        self.halt_flag = halt_flag or Event()
        self.check_in_delay = check_in_delay
        self.start_delay = start_delay if start_delay is not None else (lambda: randint(0, DEFAULT_START_DELAY_MAX))
        self.registrar = ServiceRegistrar(name=self.task_id,
                                          checkin_interval=self.check_in_delay * 2,
                                          alert_ttl=default_ttl,
                                          directory=service_registry_dir,
                                          warn_after=warn_after_checkin,
                                          error_after=error_after_checkin,
                                          critical_after=critical_after_checkin)
        self.start_checkin_thread()

    def start_checkin_thread(self):
        def _run() -> None:
            log.info(f"{self.task_id} - starting Princeps check-in thread...")
            while not self.halt_flag.wait(timeout=self.check_in_delay):
                log.info(f"{self.task_id} - checking in with Princeps")
                self.registrar.check_in()
        thread = Thread(target=_run, daemon=True)
        thread.start()

    @property
    def _start_delay(self) -> int:
        return self.start_delay if not callable(self.start_delay) else self.start_delay()

    def delay_start(self) -> None:
        delay_seconds = abs(self._start_delay)
        log.info(f"Waiting {delay_seconds} seconds before starting...")
        sleep(delay_seconds)

    @abstractmethod
    def __call__(self, func: Callable[[], None]) -> None:
        pass  # pragma: no cover


class Service(Runner):
    def __init__(self,
                 task_id: str,
                 exchange: str,
                 route: str,
                 ttl: Optional[int] = None,
                 start_delay: Union[int, Callable[[], int], None] = None,
                 relaunch_delay: int = DEFAULT_RELAUNCH_DELAY,
                 jitter: int = 3,
                 warn_after_attempts: Optional[int] = None,
                 error_after_attempts: Optional[int] = None,
                 critical_after_attempts: Optional[int] = None,
                 service_registry_dir: Optional[Path] = DEFAULT_SERVICE_REGISTRY_DIR,
                 check_in_delay: int = DEFAULT_CHECKIN_DELAY,
                 warn_after_checkin: Optional[TimeDelta] = None,
                 error_after_checkin: Optional[TimeDelta] = None,
                 critical_after_checkin: Optional[TimeDelta] = None,
                 halt_flag: Optional[Event] = None,
                 config: Optional[RobotnikConfig] = None):
        super().__init__(task_id=task_id,
                         exchange=exchange,
                         route=route,
                         default_ttl=(ttl or DEFAULT_TTL),
                         start_delay=start_delay,
                         halt_flag=halt_flag,
                         service_registry_dir=service_registry_dir,
                         check_in_delay=check_in_delay,
                         warn_after_checkin=warn_after_checkin,
                         error_after_checkin=error_after_checkin,
                         critical_after_checkin=critical_after_checkin,
                         config=config)
        self.relaunch_delay = relaunch_delay
        self.jitter = jitter
        self.warn_after_attempts = warn_after_attempts or float('inf')
        self.error_after_attempts = error_after_attempts or (1 if warn_after_attempts is None else float('inf'))
        self.critical_after_attempts = critical_after_attempts or float('inf')

    @property
    def _relaunch_delay(self) -> int:
        return self.relaunch_delay + randint(0 - self.jitter, self.jitter)

    def delay_relaunch(self):
        sleep(abs(self._relaunch_delay))

    def key(self, task_id: str) -> List[str]:
        return [hostname(), 'legion', 'service_failure', task_id]

    def __call__(self, func: Callable[[], None]) -> Callable[[], None]:
        @wraps(func)
        def retry_infinity_wrapper() -> None:
            last_traceback: Optional[str] = None
            self.delay_start()
            for i in count(1):  # pragma: no branch
                if self.halt_flag.is_set():
                    break
                try:
                    func()
                except Exception as exc:
                    log.exception(exc)
                    last_traceback = format_exc()
                finally:
                    contents = {"task_id": self.task_id,
                                "last_stack_trace": last_traceback,
                                "num_failures": i}
                    if i == 1:
                        desc = f"Service '{self.task_id}' stopped running"
                    else:
                        desc = f"Service '{self.task_id}' stopped running {i} times in a row"
                    if i >= self.critical_after_attempts:
                        self.broadcast_critical(contents=contents, desc=desc)
                    elif i >= self.error_after_attempts:
                        self.broadcast_error(contents=contents, desc=desc)
                    elif i >= self.warn_after_attempts:
                        self.broadcast_warning(contents=contents, desc=desc)
                    self.delay_relaunch()

        return retry_infinity_wrapper


class Periodic(Runner):
    """
    A decorator class which takes a callable, and executes it periodically on a delay (NOT an interval). This class is
    also capable of reporting on errors when they occur.
    """
    def __init__(self,
                 task_id: str,
                 exchange: str,
                 route: str,
                 delay: int,
                 ttl: Optional[int] = None,
                 start_delay: Union[int, Callable[[], int], None] = None,
                 relaunch_delay: int = DEFAULT_RELAUNCH_DELAY,
                 jitter: Optional[int] = None,
                 warn_after_failures: Union[int, float, None] = None,
                 error_after_failures: Union[int, float, None] = None,
                 critical_after_failures: Union[int, float, None] = None,
                 service_registry_dir: Optional[Path] = DEFAULT_SERVICE_REGISTRY_DIR,
                 check_in_delay: Optional[int] = None,
                 warn_after_checkin: Optional[TimeDelta] = None,
                 error_after_checkin: Optional[TimeDelta] = None,
                 critical_after_checkin: Optional[TimeDelta] = None,
                 halt_flag: Optional[Event] = None,
                 config: Optional[RobotnikConfig] = None):
        super().__init__(task_id=task_id,
                         exchange=exchange,
                         route=route,
                         default_ttl=(ttl or delay * 4),
                         start_delay=start_delay,
                         halt_flag=halt_flag,
                         service_registry_dir=service_registry_dir,
                         check_in_delay=(check_in_delay or delay * 2),
                         warn_after_checkin=warn_after_checkin,
                         error_after_checkin=error_after_checkin,
                         critical_after_checkin=critical_after_checkin,
                         config=config)
        self.delay = delay
        self.jitter = jitter if jitter is not None else 3
        self.relaunch_delay = relaunch_delay
        self.warn_after_failures = warn_after_failures or float('inf')
        self.error_after_failures = error_after_failures or (1 if warn_after_failures is None else float('inf'))
        self.critical_after_failures = critical_after_failures or float('inf')

    def jittery_delay(self):
        sleep(abs(self.delay + randint(0 - self.jitter, self.jitter)))

    def jittery_error_delay(self):
        sleep(abs(self.relaunch_delay + randint(0 - self.jitter, self.jitter)))

    def key(self, task_id: str) -> List[str]:
        return [hostname(), 'legion', 'periodic_task_failure', task_id]

    def __call__(self, func: Callable[[], None]) -> Callable[[], None]:
        @wraps(func)
        def run_infinity_wrapper() -> None:
            num_failures = 0
            self.delay_start()
            for _ in count():  # pragma: no branch
                if self.halt_flag.is_set():
                    break
                try:
                    func()
                    num_failures = 0
                    self.jittery_delay()
                except Exception as exc:
                    log.exception(exc)
                    num_failures += 1
                    contents = {"task_id": self.task_id,
                                "last_stack_trace": format_exc(),
                                "num_failures": num_failures}
                    desc = f"Periodic task '{self.task_id}' failed {num_failures} times in a row"
                    if num_failures >= self.critical_after_failures:
                        self.broadcast_critical(contents=contents, desc=desc)
                    elif num_failures >= self.error_after_failures:
                        self.broadcast_error(contents=contents, desc=desc)
                    elif num_failures >= self.warn_after_failures:
                        self.broadcast_warning(contents=contents, desc=desc)
                    self.jittery_error_delay()
        return run_infinity_wrapper
