from django.contrib.auth import get_user_model
from factory import Factory, Faker, LazyAttribute, SubFactory

from xiangqi import models


class UserFactor(Factory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ("username",)

    first_name = Faker('first_name')
    first_name = Faker('last_name')
    email = Faker('email')
    username = LazyAttribute(lambda f: f.email.split('@')[0])


class PlayerFactory(Factory):
    class Meta:
        model = models.Player

    user = SubFactory(UserFactor)
    rating = 1500


class ResultFactory(Factory):
    class Meta:
        model = models.Result

    description = Faker('sentence')


class GameFactory(Factory):
    class Meta:
        model = models.Game

    start_time = None
    end_time = None
    player_limit = 2
    created_by = SubFactory(PlayerFactory)
    board_dimensions = '10,9'
    move_time_limit = None
    game_time_limit = None
    result = None


class ParticipantFactory(Factory):
    class Meta:
        model = models.Participant

    score = 0.0


class PieceFactory(Factory):
    class Meta:
        model = models.Piece


class MoveTypeFactory(Factory):
    class Meta:
        model = models.MoveType


class MoveFactory(Factory):
    class Meta:
        model = models.Move
