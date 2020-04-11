import attr

from xiangqi.lib import pyffish


@attr.s(kw_only=True)
class LegalMoves:
    _fen = attr.ib()

    def result(self):
        return pyffish.legal_moves(self._fen, [])
