import json
from functools import partial
from itertools import chain

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
        return [
            {
                'player': data.get('participant', [None, None])[1],
                # {
                #     'name': data['participant'][1],
                #     'color': data['participant'],
                # },
                'origin': data.get('origin'),
                'destination': data.get('destination'),
                'move': data.get('name'),
                'fen': data['fen'],
                'legal_moves': data['legal_moves'],
            }
            for data in self._complete_game_moves_data
        ]

    @cached_property
    def _complete_game_moves_data(self):
        return [
            {'fen': fen, 'legal_moves': legal_moves, **move_data.get('fields', {})}
            for move_data, fen, legal_moves in zip(
                chain([{}], self._game_moves_data), self._fens, self._legal_moves
            )
        ]

    pass

    @cached_property
    def _game_moves_data(self):
        return json.loads(serialize(self._game_moves))

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
