from copy import deepcopy
from itertools import groupby

from django.utils.functional import cached_property
from django.views.generic.detail import SingleObjectMixin

from xiangqi import models


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
            result[move.origin.rank][move.origin.file] = None
            result[move.destination.rank][move.destination.file] = move.piece

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
