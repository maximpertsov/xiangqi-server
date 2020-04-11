from functools import partial

import pyffish

VARIANT = "xiangqi"

get_fen = partial(pyffish.get_fen, VARIANT)
gives_check = partial(pyffish.gives_check, VARIANT)
legal_moves = partial(pyffish.legal_moves, VARIANT)
start_fen = partial(pyffish.start_fen, VARIANT)
