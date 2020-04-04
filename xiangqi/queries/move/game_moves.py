from itertools import chain

import attr
from django.utils.functional import cached_property

from xiangqi.models.color import Color
from xiangqi.queries.move.serialize_move import SerializeInitialPlacement, SerializeMove


@attr.s(kw_only=True)
class GameMoves:
    class InvalidPlayer(Exception):
        pass

    _game = attr.ib()

    def result(self):
        result = []
        game_moves = chain([None], self._game_moves)

        for move, new_move in zip(game_moves, self._new_moves):
            new_move.update(self._move_data(move))
            result.append(new_move)

        return result

    def _move_data(self, move=None):
        result = {"move": None, "player": None}
        if move:
            result.update(
                {
                    "move": move.name,
                    "player": {
                        "name": move.player.username,
                        "color": self._player_color(move),
                    },
                }
            )
        return result

    def _player_color(self, move):
        # TODO: .value?
        if move.player == self._game.red_player:
            return Color.RED.value
        if move.player == self._game.black_player:
            return Color.BLACK.value

        raise self.InvalidPlayer

    @property
    def _new_moves(self):
        result = [self._initial_move]
        for move in self._game_moves:
            previous_fen = result[-1]["fen"]
            new_move = SerializeMove(fen=previous_fen, move_name=move.name).result()
            result.append(new_move)

        return result

    @cached_property
    def _game_moves(self):
        return self._game.move_set.all()

    @property
    def _initial_move(self):
        return SerializeInitialPlacement().result()
