from functools import partial
from inspect import getmembers
from types import SimpleNamespace

import pyffish

VARIANT = "xiangqi"

export_functions = ["get_fen", "gives_check", "legal_moves", "start_fen"]


class XiangqiError(Exception):
    """
    Exception of all Xiangqi game logic errors
    """


def wrap_system_errors(func):
    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SystemError as error:
            raise XiangqiError(str(error.__cause__))

    return wrapped


xiangqi = SimpleNamespace(
    Error=XiangqiError,
    **{
        key: wrap_system_errors(partial(func, VARIANT))
        for key, func in getmembers(pyffish)
        if key in export_functions
    }
)
