import pyffish

from xiangqi.queries.move.legal_moves import LegalMoves


class CreateMove:
    def __init__(self, fen, move):
        self._fen = fen
        self._move = move

    def result(self):
        return {
            'fen': self._new_fen,
            'legal_moves': self._legal_moves,
            'move': self._move,
        }

    @property
    def _new_fen(self):
        return pyffish.get_fen('xiangqi', self._fen, [self._move])

    @property
    def _legal_moves(self):
        return LegalMoves(fen=self._fen, moves=[self._move]).result()
