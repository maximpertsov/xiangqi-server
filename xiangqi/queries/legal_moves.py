import attr
import pyffish


@attr.s(kw_only=True)
class LegalMoves:
    _fen = attr.ib()
    _moves = attr.ib()

    def result(self):
        return pyffish.legal_moves("xiangqi", self._fen, self._moves)
