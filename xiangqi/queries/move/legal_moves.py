from functools import partial
from itertools import chain

import pyffish
from django.utils.functional import cached_property

get_fen = partial(pyffish.get_fen, "xiangqi")
start_fen = partial(pyffish.start_fen, "xiangqi")
legal_moves = partial(pyffish.legal_moves, "xiangqi")


class LegalMoves:
    def __init__(self, fen):
        self._fen = fen

    def result(self):
        return None
