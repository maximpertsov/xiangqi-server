import json
import os
from copy import deepcopy
from itertools import groupby

from django.conf import settings
from django.core.serializers import serialize
from django.http import JsonResponse
from django.utils.functional import cached_property
from django.views.generic import DetailView

from xiangqi import models


def load_fixture(fixture):
    fixture_path = os.path.join(settings.BASE_DIR, 'xiangqi/fixtures', fixture)
    with open(fixture_path) as f:
        return json.load(f)


def allow_cross_origin(f):
    def wrapped(*args, **kwargs):
        response = f(*args, **kwargs)
        response["Access-Control-Allow-Origin"] = "http://localhost:3000"
        response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
        return response

    return wrapped


class Game(DetailView):
    model = models.Game

    @staticmethod
    def parse_position(position):
        # TODO: return None if parsing fails?
        return [int(dim.strip()) for dim in position.split(',')]

    @cached_property
    def game(self):
        return self.get_object()

    @cached_property
    def ranks(self):
        ranks, _ = self.parse_position(self.game.board_dimensions)
        return ranks

    @cached_property
    def files(self):
        _, files = self.parse_position(self.game.board_dimensions)
        return files

    @property
    def moves(self):
        return self.game.move_set.select_related('piece').order_by('order')

    @cached_property
    def initial_board(self):
        result = [[None for _ in range(self.files)] for _ in range(self.ranks)]
        for piece in models.Piece.objects.all():
            rank, file = self.parse_position(piece.starting_position)
            result[rank][file] = piece.name
        return result

    @property
    def current_position(self):
        result = deepcopy(self.initial_board)
        for move in self.moves:
            from_rank, from_file = self.parse_position(move.from_position)
            to_rank, to_file = self.parse_position(move.to_position)
            result[from_rank][from_file] = None
            result[to_rank][to_file] = move.piece.name

        return result

    def fen_rank(self, rank):
        return ''.join(
            str(sum(1 for _ in g)) if p is None else p for p, g in groupby(rank)
        )

    @property
    def current_position_fen(self):
        return '/'.join(self.fen_rank(rank) for rank in self.current_position)

    @property
    def participants(self):
        return self.game.participant_set.select_related('player', 'player__user').all()

    @property
    def players_data(self):
        result = []
        for participant in self.participants:
            result.append(
                {
                    'name': participant.player.user.username,
                    'color': participant.role,
                    'score': participant.score,
                }
            )
        return result

    @allow_cross_origin
    def get(self, request, pk):
        serialized = json.loads(serialize('json', [self.game]))
        result = serialized[0]['fields']
        del result['board_dimensions']
        result['ranks'] = self.ranks
        result['files'] = self.files
        result['fen'] = self.current_position_fen
        result['players'] = self.players_data
        return JsonResponse(result, status=200)
