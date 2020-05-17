from itertools import chain

import attr
from django.utils.functional import cached_property

from xiangqi.queries.serialize_move import SerializeInitialPlacement, SerializeMove


@attr.s(kw_only=True)
class GameMoves:
    _game = attr.ib()

    def result(self):
        result = []
        game_moves = chain([None], self._game_moves)

        for move, new_move in zip(game_moves, self._new_moves):
            new_move.update(self._move_data(move))
            result.append(new_move)

        return result

    def _move_data(self, move=None):
        result = {"fan": None, "player_name": None}
        if move:
            result.update({"fan": move.fan, "player_name": move.player.username})
        return result

    @property
    def _new_moves(self):
        result = [self._initial_move]
        for move in self._game_moves:
            previous_fen = result[-1]["fen"]
            new_move = SerializeMove(fan=move.fan, fen=previous_fen).result()
            result.append(new_move)

        return result

    @cached_property
    def _game_moves(self):
        return self._game.move_set.all()

    @cached_property
    def _initial_move(self):
        return SerializeInitialPlacement().result()
