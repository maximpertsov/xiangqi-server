import attr

from lib.pyffish import xiangqi
from xiangqi.queries.serialize_fen import SerializeFen, SerializeInitialFen


@attr.s(kw_only=True)
class SerializeMove:
    _fan = attr.ib()
    _fen = attr.ib()

    def result(self):
        return {**self._fen_data, "fan": self._fan}

    @property
    def _fen_data(self):
        return SerializeFen(fen=self._next_fen).result()

    @property
    def _next_fen(self):
        return xiangqi.get_fen(self._fen, [self._fan])


class SerializeInitialPlacement:
    def result(self):
        return {**self._fen_data, "fan": None}

    @property
    def _fen_data(self):
        return SerializeInitialFen().result()
