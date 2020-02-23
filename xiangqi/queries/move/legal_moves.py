import pyffish


class LegalMoves:
    def __init__(self, fen, moves):
        self._fen = fen
        self._moves = moves

    def result(self):
        return pyffish.legal_moves("xiangqi", self._fen, self._moves)
