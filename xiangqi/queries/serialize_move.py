import attr

from xiangqi.lib.pyffish import xiangqi
from xiangqi.queries.serialize_fen import SerializeFen, SerializeInitialFen


@attr.s(kw_only=True)
class SerializeMove:
    _fen = attr.ib()
    _move_name = attr.ib()

    def result(self):
        return {**self._fen_data, "move": self._move_name}

    @property
    def _fen_data(self):
        return SerializeFen(fen=self._next_fen).result()

    @property
    def _next_fen(self):
        return xiangqi.get_fen(self._fen, [self._move_name])


class SerializeInitialPlacement:
    def result(self):
        return {**self._fen_data, "move": None}

    @property
    def _fen_data(self):
        return SerializeInitialFen().result()
