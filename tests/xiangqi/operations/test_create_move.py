import pytest
from django.core.exceptions import ValidationError

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
    return {"move": "b10c8", "player": red_player.username}


@pytest.fixture
def event(game_with_players, payload, game_event_factory):
    return game_event_factory(game=game_with_players, payload=payload, name="move")


@pytest.fixture
def mock_pyffish(mocker):
    return mocker.patch.multiple(
        "xiangqi.lib.pyffish.xiangqi",
        get_fen=mocker.DEFAULT,
        gives_check=mocker.DEFAULT,
        start_fen=mocker.DEFAULT,
    )


@pytest.mark.django_db
def test_create_move(event, mock_pyffish):
    assert event.game.move_set.count() == 0

    mock_pyffish["start_fen"].return_value = "start fen"
    mock_pyffish["get_fen"].return_value = "next fen"
    mock_pyffish["gives_check"].return_value = False

    CreateMove(event=event).perform()
    mock_pyffish["start_fen"].assert_called_once_with()
    mock_pyffish["get_fen"].assert_called_once_with("start fen", ["b10c8"])
    mock_pyffish["gives_check"].assert_called_once_with("next fen", [])

    first_move = event.game.move_set.first()
    assert first_move.name == "b10c8"
    assert first_move.fen == "next fen"
    assert first_move.gives_check is False

    assert event.game.move_set.count() == 1


@pytest.fixture
def event_with_non_player(game_with_players, payload, game_event_factory):
    payload.update(player="Not a game player")
    return game_event_factory(game=game_with_players, payload=payload, name="move")


@pytest.mark.django_db
def test_create_move_non_participant(event_with_non_player):
    with pytest.raises(ValidationError):
        CreateMove(event=event_with_non_player).perform()
