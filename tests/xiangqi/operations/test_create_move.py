import pytest
from django.core.cache import cache
from django.core.exceptions import ValidationError

from xiangqi.operations.create_move import CreateMove


@pytest.fixture
def game_with_players(game, participant_factory, player_factory):
    p1, p2 = player_factory.create_batch(2)
    participant_factory(game=game, player=p1, color="red")
    participant_factory(game=game, player=p2, color="black")
    return game


@pytest.fixture
def participant(game_with_players):
    return game_with_players.participant_set.first()


@pytest.fixture
def payload(participant):
    return {"move": "b10c8", "player": participant.player.user.username}


@pytest.fixture
def event(game_with_players, payload, game_event_factory):
    return game_event_factory(game=game_with_players, payload=payload, name="move")


@pytest.mark.django_db
def test_create_move(mocker, event, participant):
    mock_cache_set = mocker.patch.object(cache, "set")

    assert event.game.move_set.count() == 0

    CreateMove(event=event).perform()
    mock_cache_set.assert_called_once_with(
        "updated_at_{}".format(event.game.slug), 1, timeout=3600
    )
    assert event.game.move_set.first().name == "b10c8"
    assert event.game.move_set.count() == 1


@pytest.fixture
def event_with_non_player(game_with_players, payload, game_event_factory):
    payload.update(player="Not a game player")
    return game_event_factory(game=game_with_players, payload=payload, name="move")


@pytest.mark.django_db
def test_create_move_non_participant(event_with_non_player):
    with pytest.raises(ValidationError):
        CreateMove(event=event_with_non_player).perform()
