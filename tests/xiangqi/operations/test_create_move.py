import pytest
from rest_framework.exceptions import ValidationError

from xiangqi.operations.create_move import CreateMove


@pytest.fixture
def red_player(player_factory):
    return player_factory()


@pytest.fixture
def black_player(player_factory):
    return player_factory()


@pytest.fixture
def game_with_players(game_factory, red_player, black_player):
    return game_factory(red_player=red_player, black_player=black_player)


@pytest.fixture
def payload(red_player):
    return {"uci": "b10c8", "fen": "FEN", "player": red_player.username}


@pytest.fixture
def event(game_with_players, payload, game_event_factory):
    return game_event_factory(game=game_with_players, payload=payload, name="move")


@pytest.mark.django_db
def test_create_move(event):
    assert event.game.move_set.count() == 0

    CreateMove(event=event).perform()
    assert event.game.move_set.first().uci == "b10c8"
    assert event.game.move_set.count() == 1


@pytest.fixture
def event_with_non_player(
    game_with_players, player_factory, payload, game_event_factory
):
    payload.update(player=player_factory().username)
    return game_event_factory(game=game_with_players, payload=payload, name="move")


@pytest.mark.django_db
@pytest.mark.xfail
def test_create_move_non_participant(event_with_non_player):
    with pytest.raises(ValidationError):
        CreateMove(event=event_with_non_player).perform()
