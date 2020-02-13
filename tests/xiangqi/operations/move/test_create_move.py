import pytest
from django.core.exceptions import ValidationError
from django.core.management import call_command
from pytest_factoryboy import register

from tests import factories
from xiangqi.models import Move
from xiangqi.operations.move import CreateMove

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
def game_with_players(game, participant_factory, player_factory):
    p1, p2 = player_factory.create_batch(2)
    participant_factory(game=game, player=p1, color='red')
    participant_factory(game=game, player=p2, color='black')
    return game


@pytest.fixture
def participant(game_with_players):
    return game_with_players.participant_set.first()


@pytest.fixture
def payload():
    return {"from": [0, 1], "to": [2, 2], "type": "move"}


# TODO: remove need for existing pieces
@pytest.mark.django_db
def test_create_move(game_with_players, participant, payload, pieces):
    assert Move.objects.count() == 0
    payload.update(player=participant.player.user.username)
    CreateMove(game_with_players, payload).perform()
    assert Move.objects.count() == 1


@pytest.mark.django_db
def test_create_move_non_participant(game_with_players, payload, pieces):
    payload.update(player="Not a game player")
    with pytest.raises(ValidationError):
        CreateMove(game_with_players, payload).perform()
