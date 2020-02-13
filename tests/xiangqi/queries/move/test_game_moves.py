import pytest
from django.core.management import call_command
from pytest_factoryboy import register

from tests import factories
from xiangqi.models import Move
from xiangqi.queries.move import GameMoves

register(factories.UserFactory)
register(factories.PlayerFactory)
register(factories.GameFactory)
register(factories.MoveFactory)
register(factories.ParticipantFactory)


# TODO: remove need for existing pieces
@pytest.fixture
def pieces(game):
    call_command('loaddata', 'pieces.json')
    return game


@pytest.fixture
def game_with_moves(game, participant_factory, move_factory, player_factory):
    p1, p2 = player_factory.create_batch(2)
    participant1 = participant_factory(game=game, player=p1, color='red')
    participant2 = participant_factory(game=game, player=p2, color='black')
    move_factory(game=game, order=1, participant=participant1, name='a1a3')
    move_factory(game=game, order=2, participant=participant2, name='a10a9')
    move_factory(game=game, order=3, participant=participant1, name='i1i3')
    return game


# TODO: remove need for existing pieces
@pytest.mark.django_db
def test_game_moves(game_with_moves, pieces):
    assert Move.objects.count() == 0
    assert GameMoves(game_with_moves).result() == [{}]
