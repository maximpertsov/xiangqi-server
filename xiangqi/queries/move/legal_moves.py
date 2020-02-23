import pyffish


class LegalMoves:
    def __init__(self, fen):
        self._fen = fen

    def result(self):
        return pyffish.legal_moves("xiangqi", self._fen, [])
