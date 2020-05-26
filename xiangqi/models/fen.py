import attr
from django.utils.functional import cached_property

from xiangqi.models.color import Color


@attr.s(kw_only=True)
class Fen:
    class Error(Exception):
        pass

    _fen = attr.ib()

    @property
    def active_color(self):
        if self._properties["active_color"] == "w":
            return Color.RED.value
        if self._properties["active_color"] == "b":
            return Color.BLACK.value
        return self.Error("Cannot determine color")

    @property
    def fullmoves(self):
        return int(self._properties["fullmoves"])

    @cached_property
    def _properties(self):
        return dict(zip(self._fields, self._fen.split()))

    @property
    def _fields(self):
        return [
            "placement",
            "active_color",
            "castling",
            "en_passant",
            "halfmoves",
            "fullmoves",
        ]
