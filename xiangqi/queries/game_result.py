import attr
from django.utils.functional import cached_property

from lib.pyffish import xiangqi


@attr.s(kw_only=True)
class GameResult:
    class Error(Exception):
        pass

    _fen = attr.ib()

    @property
    def result(self):
        return self._score

    @property
    def _score(self):
        # import pdb; pdb.set_trace()
        if self._has_legal_moves:
            return [0.5, 0.5] if self._is_draw else [0, 0]
        if self._color == "w":
            return [0, 1]
        if self._color == "b":
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

    @cached_property
    def _has_legal_moves(self):
        return bool(xiangqi.legal_moves(self._fen, []))

    @property
    def _color(self):
        return self._fen.split()[1]
