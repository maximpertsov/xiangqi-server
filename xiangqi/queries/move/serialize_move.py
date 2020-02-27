import pyffish

from xiangqi.queries.move.legal_moves import LegalMoves


class SerializeMove:
    # TODO: define another query that does not require a fen and instead
    # derives everything from all moves up until this point
    def __init__(self, fen, move):
        self._fen = fen
        self._move = move

    def result(self):
        return {
            'fen': self._new_fen,
            'legal_moves': self._legal_moves,
            'move': self._move_name,
        }

    @property
    def _new_fen(self):
        return pyffish.get_fen('xiangqi', self._fen, [self._move_name])

    @property
    def _legal_moves(self):
        return LegalMoves(fen=self._fen, moves=[self._move_name]).result()

    @property
    def _move_name(self):
        return self._move.name
