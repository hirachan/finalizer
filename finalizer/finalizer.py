from __future__ import annotations
from typing import Callable, Any
import signal
import sys
from contextlib import ContextDecorator


def sig_handler(signum, frame) -> None:
    sys.exit(1)


class Finalizer(ContextDecorator):
    def __init__(self, func: Callable[..., None], *args, **kw):
        self.__cleanup: Callable[..., None] = func
        self.__args: tuple[Any, ...] = args
        self.__kw: dict[str, Any] = kw
        self.__prev_sigterm: signal.Handlers = signal.SIG_DFL

    def __enter__(self):
        self.__prev_sigterm = signal.getsignal(signal.SIGTERM)
        signal.signal(signal.SIGTERM, sig_handler)

    def __exit__(self, exc_type, exc_value, traceback):
        cur_sigint = signal.getsignal(signal.SIGINT)
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        self.__cleanup(*self.__args, **self.__kw)
        signal.signal(signal.SIGTERM, self.__prev_sigterm)
        signal.signal(signal.SIGINT, cur_sigint)
