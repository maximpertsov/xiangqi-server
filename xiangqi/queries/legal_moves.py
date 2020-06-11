from lib.pyffish import xiangqi


class LegalMoves:
    def result(self, fen):
        self._fen = fen
        return {move: xiangqi.get_fen(self._fen, [move]) for move in self._legal_moves}

    @property
    def _legal_moves(self):
        return xiangqi.legal_moves(self._fen, [])
