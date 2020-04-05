import attr

from xiangqi.models.color import Color


@attr.s(kw_only=True)
class GamePlayers:
    _game = attr.ib()

    def result(self):
        return [
            {"name": self._game.red_player.username, "color": Color.RED.value},
            {"name": self._game.black_player.username, "color": Color.BLACK.value},
        ]
