import attr
from django.utils.functional import cached_property

from xiangqi.models.team import Team


@attr.s(kw_only=True)
class Fen:
    class Error(Exception):
        pass

    _fen = attr.ib()

    @property
    def active_team(self):
        if self._properties["active_team"] == "w":
            return Team.RED.value
        if self._properties["active_team"] == "b":
            return Team.BLACK.value
        return self.Error("Cannot determine team")

    @cached_property
    def _properties(self):
        return dict(zip(self._fields, self._fen.split()))

    @property
    def _fields(self):
        return [
            "placement",
            "active_team",
            "castling",
            "en_passant",
            "halfmoves",
            "fullmoves",
        ]
