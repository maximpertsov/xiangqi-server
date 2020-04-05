import attr

from xiangqi.models.color import Color


@attr.s(kw_only=True)
class GamePlayers:
    _game = attr.ib()

    def result(self):
        pass
