from functools import partial
from inspect import getmembers
from types import SimpleNamespace

import pyffish

VARIANT = "xiangqi"

export_functions = ["get_fen", "gives_check", "legal_moves", "start_fen"]

xiangqi = SimpleNamespace(
    **{
        key: partial(func, VARIANT)
        for key, func in getmembers(pyffish)
        if key in export_functions
    }
)
