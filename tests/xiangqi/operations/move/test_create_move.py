from unittest.mock import patch

import pytest
from django.core.cache import cache
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
    return {"move": "b10c8"}


# TODO: remove need for existing pieces
@pytest.mark.django_db
def test_create_move(game_with_players, participant, payload, pieces):
    assert Move.objects.count() == 0
    payload.update(player=participant.player.user.username)
    with patch.object(cache, 'set') as mock_cache_set:
        CreateMove(game_with_players, payload).perform()
        mock_cache_set.assert_called_once_with(
            "updated_at_{}".format(game_with_players.slug), 1, timeout=None
        )
        # TODO: temporary?
        assert Move.objects.first().name == 'b10c8'
        assert Move.objects.count() == 1


@pytest.mark.django_db
def test_create_move_non_participant(game_with_players, payload, pieces):
    payload.update(player="Not a game player")
    with pytest.raises(ValidationError):
        CreateMove(game_with_players, payload).perform()
