from functools import partial
from itertools import chain

import pyffish
from django.utils.functional import cached_property

from xiangqi.queries.move.legal_moves import LegalMoves

get_fen = partial(pyffish.get_fen, "xiangqi")
start_fen = partial(pyffish.start_fen, "xiangqi")


class GameMoves:
    def __init__(self, game):
        self._game = game

    def result(self):
        result = []
        game_moves = chain([None], self._game_moves)

        for move, fen, legal_moves in zip(game_moves, self._fens, self._legal_moves):
            data = {"fen": fen, "legal_moves": legal_moves}
            if move:
                data.update(self._move_data(move))
            result.append(data)

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
    def _fens(self):
        result = [start_fen()]
        for move in self._game_moves:
            fen = get_fen(result[-1], [move.name])
            result.append(fen)
        return result

    @cached_property
    def _legal_moves(self):
        return [LegalMoves(fen=fen, moves=[]).result() for fen in self._fens]
