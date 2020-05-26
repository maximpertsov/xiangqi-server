import attr
from django.utils.functional import cached_property

from lib.pyffish import xiangqi


@attr.s(kw_only=True)
class CurrentMoveFen:
    _game = attr.ib()

    @property
    def result(self):
        if self._last_move is None:
            return xiangqi.start_fen()
        return self._last_move.fen

    @cached_property
    def _last_move(self):
        return self._game.move_set.order_by("-pk").first()
