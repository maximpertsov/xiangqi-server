import json
from copy import deepcopy
from functools import partial
from itertools import groupby

import jsonschema
from django.core import serializers
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.utils.functional import cached_property
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.detail import SingleObjectMixin, View

from xiangqi import models

serialize = partial(serializers.serialize, 'json', use_natural_foreign_keys=True)
deserialize = partial(serializers.deserialize, 'json', use_natural_foreign_keys=True)


class GameMixin(SingleObjectMixin):
    model = models.Game

    @staticmethod
    def parse_position(position):
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
        return self.game.move_set.select_related(
            'piece', 'origin', 'destination'
        ).order_by('order')

    @cached_property
    def initial_board(self):
        result = [[None for _ in range(self.files)] for _ in range(self.ranks)]
        for piece in models.Piece.objects.all().select_related('origin'):
            result[piece.origin.rank][piece.origin.file] = piece
        return result

    @property
    def current_board(self):
        result = deepcopy(self.initial_board)
        for move in self.moves.select_related('origin', 'destination'):
            from_rank, from_file = self.parse_position(move.origin)
            to_rank, to_file = self.parse_position(move.destination)
            result[from_rank][from_file] = None
            result[to_rank][to_file] = move.piece

        return result

    @staticmethod
    def fen_rank(rank):
        return ''.join(
            str(sum(1 for _ in g)) if p is None else p.name for p, g in groupby(rank)
        )

    def board_fen(self, board):
        return '/'.join(self.fen_rank(rank) for rank in board)

    @property
    def participants(self):
        return self.game.participant_set.select_related('player', 'player__user').all()

    @property
    def active_participant(self):
        if self.moves.exists():
            last_move_participant = self.moves.last().participant
            return self.participants.exclude(pk=last_move_participant.pk).first()
        return self.participants.filter(color='red').first()

    @cached_property
    def players_data_by_participant(self):
        return {
            tuple(participant.natural_key()): {
                'name': participant.player.user.username,
                'color': participant.color,
                'score': participant.score,
            }
            for participant in self.participants
        }


@method_decorator(csrf_exempt, name="dispatch")
class GameView(GameMixin, View):
    @cached_property
    def cache_key(self):
        return 'initial_fen_{}'.format(self.kwargs[self.slug_url_kwarg])

    @cached_property
    def initial_fen(self):
        result = cache.get(self.cache_key)
        if result is None:
            result = self.board_fen(self.initial_board)
            cache.set(self.cache_key, result, 100)
        return result

    def get(self, request, slug):
        serialized = serialize([self.game])
        result = json.loads(serialized)[0]['fields']
        del result['board_dimensions']
        result['ranks'] = self.ranks
        result['files'] = self.files
        result['initial_fen'] = self.initial_fen
        result['players'] = list(self.players_data_by_participant.values())
        # TODO add test
        result['active_color'] = getattr(self.active_participant, 'color', 'red')
        return JsonResponse(result, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class GameMoveView(GameMixin, View):
    @property
    def post_schema(self):
        return {
            "properties": {
                "player": {"type": "string"},
                "from": {
                    "type": "array",
                    "items": {"type": "number"},
                    "minItems": 2,
                    "maxItems": 2,
                },
                "to": {
                    "type": "array",
                    "items": {"type": "number"},
                    "minItems": 2,
                    "maxItems": 2,
                },
                "piece": {"type": "string"},
                "type": {"type": "string"},
            },
            "required": ["player", "from", "to", "piece", "type"],
            "additionalProperties": False,
        }

    def position(self, rank, file):
        result, _ = models.Position.objects.get_or_create(rank=rank, file=file)
        return result

    def get(self, request, slug):
        serialized = serialize(self.moves.all())
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
                }
            )

        return JsonResponse({'moves': moves}, status=200)

    def validate_data(self, payload, slug):
        username = payload.pop('player')
        payload.update(participant=[slug, username])
        payload['origin'] = payload.pop('from')
        payload['destination'] = payload.pop('to')
        piece_name = payload.pop('piece')

        try:
            participant = self.participants.get(player__user__username=username)
        except models.Participant.DoesNotExist:
            raise ValidationError('Invalid player')

        if self.active_participant != participant:
            raise ValidationError('Moving out of turn')

        from_rank, from_file = payload['origin']
        to_rank, to_file = payload['destination']
        piece = self.current_board[from_rank][from_file]
        if piece.name != piece_name:
            raise ValidationError('Invalid move')

        payload['piece'] = piece.pk
        payload['type'] = models.MoveType.objects.get_or_create(
            name=payload.pop('type')
        )[0].pk
        payload['order'] = self.moves.count() + 1
        payload['notation'] = 'rank,file->rank,file'
        payload['game'] = [slug]

    def post(self, request, slug):
        try:
            payload = json.loads(request.body.decode("utf-8"))
            jsonschema.validate(payload, self.post_schema)
            self.validate_data(payload, slug)
        except json.JSONDecodeError:
            return JsonResponse({"error": 'Error parsing request'}, status=400)
        except (jsonschema.ValidationError, ValidationError) as e:
            return JsonResponse({"error": str(e)}, status=400)

        data = {'model': 'xiangqi.move', 'fields': payload}

        try:
            deserialized = deserialize(json.dumps([data]))
            for obj in deserialized:
                obj.object.save()
                return JsonResponse({}, status=201)
        except serializers.base.DeserializationError:
            return JsonResponse({"error": "Could not save move"}, status=400)
