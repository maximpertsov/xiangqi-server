from itertools import chain

import pyffish
from django.utils.functional import cached_property

from xiangqi.queries.move.legal_moves import LegalMoves
from xiangqi.queries.move.serialize_move import SerializeMove


class GameMoves:
    def __init__(self, game):
        self._game = game

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
                        # TODO: cached get participants via lru cache?
                        "name": move.participant.player.user.username,
                        "color": move.participant.color,
                    },
                }
            )
        return result

    @cached_property
    def _game_moves(self):
        return self._game.move_set.all()

    @cached_property
    def _start_fen(self):
        return pyffish.start_fen("xiangqi")

    @property
    def _new_moves(self):
        result = [self._initial_move]
        for move in self._game_moves:
            previous_fen = result[-1]["fen"]
            new_move = SerializeMove(fen=previous_fen, move_name=move.name).result()
            result.append(new_move)

        return result

    @property
    def _initial_move(self):
        return {
            "fen": self._start_fen,
            "legal_moves": LegalMoves(fen=self._start_fen, moves=[]).result(),
        }
