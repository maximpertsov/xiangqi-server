import attr
from django.utils.functional import cached_property

from xiangqi.models.color import Color
from xiangqi.models.fen import Fen


@attr.s(kw_only=True)
class MoveOrder:
    class Error(Exception):
        pass

    _fen = attr.ib()

    @property
    def result(self):
        return self._fullmoves * 2 - (1 if self._active_color == Color.RED.value else 0)

    @property
    def _fullmoves(self):
        return self._fen_properties.fullmoves

    @property
    def _active_color(self):
        return self._fen_properties.active_color

    @cached_property
    def _fen_properties(self):
        return Fen(fen=self._fen)
