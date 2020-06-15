from django.utils.functional import cached_property

from lib.pyffish import xiangqi
from xiangqi.models.team import Team
from xiangqi.models.fen import Fen


class GameResult:
    class Error(Exception):
        pass

    def result(self, move):
        self._move = move

        return self._score

    @property
    def _score(self):
        if self._has_legal_moves:
            return [0.5, 0.5] if self._is_draw else [0, 0]
        if self._team == Team.RED.value:
            return [0, 1]
        if self._team == Team.BLACK.value:
            return [1, 0]

        raise self.Error("Cannot determine result")

    @property
    def _is_draw(self):
        if self._both_have_insufficient_material:
            return True
        return False

    @property
    def _both_have_insufficient_material(self):
        return all(xiangqi.has_insufficient_material(self._fen, []))

    @property
    def _has_legal_moves(self):
        return bool(xiangqi.legal_moves(self._fen, []))

    @cached_property
    def _team(self):
        return Fen(fen=self._fen).active_team

    @property
    def _fen(self):
        return self._move.fen
