import attr
from django.utils.functional import cached_property

from lib.pyffish import xiangqi
from xiangqi.models.color import Color
from xiangqi.models.draw_event import DrawEventTypes
from xiangqi.models.fen import Fen


@attr.s(kw_only=True)
class GameResult:
    class Error(Exception):
        pass

    _move = attr.ib()

    @property
    def result(self):
        return self._score

    @property
    def _score(self):
        if self._has_legal_moves:
            return [0.5, 0.5] if self._is_draw else [0, 0]
        if self._color == Color.RED.value:
            return [0, 1]
        if self._color == Color.BLACK.value:
            return [1, 0]

        raise self.Error("Cannot determine result")

    @property
    def _is_draw(self):
        if self._both_have_insufficient_material:
            return True
        if self._has_accepted_draw:
            return True
        return False

    @property
    def _has_accepted_draw(self):
        return self._move.game.event_set.filter(
            name=DrawEventTypes.ACCEPTED_DRAW.value
        ).exists()

    @property
    def _both_have_insufficient_material(self):
        return all(xiangqi.has_insufficient_material(self._fen, []))

    @property
    def _has_legal_moves(self):
        return bool(xiangqi.legal_moves(self._fen, []))

    @cached_property
    def _color(self):
        return Fen(fen=self._fen).active_color

    @property
    def _fen(self):
        return self._move.fen
