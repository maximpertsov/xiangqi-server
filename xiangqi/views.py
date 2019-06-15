import json
from copy import deepcopy
from itertools import groupby

from django.core.serializers import serialize
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.utils.functional import cached_property
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from xiangqi import models


@method_decorator(csrf_exempt, name="dispatch")
class GameDetailView(DetailView):
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
            result[rank][file] = piece
        return result

    @property
    def current_position(self):
        result = deepcopy(self.initial_board)
        for move in self.moves:
            from_rank, from_file = self.parse_position(move.from_position)
            to_rank, to_file = self.parse_position(move.to_position)
            result[from_rank][from_file] = None
            result[to_rank][to_file] = move.piece

        return result

    def fen_rank(self, rank):
        return ''.join(
            str(sum(1 for _ in g)) if p is None else p.name for p, g in groupby(rank)
        )

    @property
    def current_position_fen(self):
        return '/'.join(self.fen_rank(rank) for rank in self.current_position)

    @property
    def participants(self):
        return self.game.participant_set.select_related('player', 'player__user').all()

    @property
    def active_participant(self):
        if self.moves.exists():
            last_move_participant = self.moves.last().participant
            return self.participants.exclude(pk=last_move_participant.pk).first()
        return self.participants.filter(role='red').first()

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

    def get(self, request, pk):
        serialized = json.loads(serialize('json', [self.game]))
        result = serialized[0]['fields']
        del result['board_dimensions']
        result['ranks'] = self.ranks
        result['files'] = self.files
        result['fen'] = self.current_position_fen
        result['players'] = self.players_data
        # TODO add test
        result['active_color'] = getattr(self.active_participant, 'role', 'red')
        return JsonResponse(result, status=200)

    def post(self, request, pk):
        try:
            request_data = json.loads(request.body.decode("utf-8"))
            # TODO: validate with jsonschema?
            # jsonschema.validate(json_request, schema)
        except json.JSONDecodeError:
            return JsonResponse({"error": 'Error parsing request'}, status=400)
        # except jsonschema.ValidationError as e:
        #     return JsonResponse({"error": str(e)}, status=400)

        username = request_data['player']
        from_position = request_data['from']
        to_position = request_data['to']
        piece_name = request_data['piece']
        move_type = request_data['type']

        try:
            participant = self.participants.get(player__user__username=username)
        except models.Participant.DoesNotExist:
            return JsonResponse({"error": 'Invalid player'}, status=400)

        if self.active_participant != participant:
            return JsonResponse({"error": 'Moving out of turn'}, status=400)

        from_rank, from_file = self.parse_position(from_position)
        to_rank, to_file = self.parse_position(from_position)
        piece = self.current_position[from_rank][from_file]
        if piece.name != piece_name:
            return JsonResponse({"error": 'Invalid move'}, status=400)

        models.Move.objects.create(
            game=self.game,
            participant=participant,
            piece=piece,
            # TODO: receiving from client, but maybe this should be generated server-side?
            type=models.MoveType.objects.get_or_create(name=move_type)[0],
            # TODO: either order by red + black move, or drop entirely
            order=self.moves.count() + 1,
            notation='rank,file->rank,file',
            from_position=from_position,
            to_position=to_position,
        )
        return JsonResponse({}, status=201)
