import attr

from xiangqi.lib import pyffish


@attr.s(kw_only=True)
class LegalMoves:
    _fen = attr.ib()

    def result(self):
        return {move: pyffish.get_fen(self._fen, [move]) for move in self._legal_moves}

    @property
    def _legal_moves(self):
        return pyffish.legal_moves(self._fen, [])
