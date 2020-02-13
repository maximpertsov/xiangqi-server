import json
from functools import partial

import pyffish
from django.core import serializers
from django.utils.functional import cached_property

serialize = partial(serializers.serialize, 'json', use_natural_foreign_keys=True)

get_fen = partial(pyffish.get_fen, 'xiangqi')
start_fen = partial(pyffish.start_fen, 'xiangqi')
legal_moves = partial(pyffish.legal_moves, 'xiangqi')


class GameMoves:
    def __init__(self, game):
        self._game = game

    def result(self):
        serialized = serialize(self._game_moves)
        moves = []
        for data in json.loads(serialized):
            fields = data.pop('fields')
            participant_key = tuple(fields['participant'])
            player = dict(self.players_data_by_participant[participant_key])
            del player['score']

            moves.append(
                {
                    'player': player,
                    'origin': fields['origin'],
                    'destination': fields['destination'],
                    'name': fields['name'],
                }
            )

        return moves

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
        return [legal_moves(fen, []) for fen in self._fens]

    # TODO: make a batch call to ffish
    @cached_property
    def _san_moves(self):
        pass
