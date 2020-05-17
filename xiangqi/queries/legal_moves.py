import attr

from lib.pyffish import xiangqi


@attr.s(kw_only=True)
class LegalMoves:
    _fen = attr.ib()

    def result(self):
        return {move: xiangqi.get_fen(self._fen, [move]) for move in self._legal_moves}

    @property
    def _legal_moves(self):
        return xiangqi.legal_moves(self._fen, [])
