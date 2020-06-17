import pytest
from rest_framework.exceptions import ValidationError

from xiangqi.operations.handle_move import HandleMove
from xiangqi.queries.game_result import GameResult


@pytest.fixture
def mock_game_continues(mocker):
    return mocker.patch.object(GameResult, "result", return_value=[0, 0])


@pytest.fixture
def player1(player_factory):
    return player_factory()


@pytest.fixture
def player2(player_factory):
    return player_factory()


@pytest.fixture
def game_with_players(game_factory, player1, player2):
    return game_factory(player1=player1, player2=player2)


@pytest.fixture
def payload(player1):
    return {"uci": "b10c8", "fen": "FEN", "player": player1.username}


@pytest.fixture
def event(game_with_players, payload, game_event_factory):
    return game_event_factory(game=game_with_players, payload=payload, name="move")


@pytest.mark.django_db
def test_create_move(mock_game_continues, event):
    assert event.game.move_set.count() == 0

    HandleMove().perform(event=event)
    mock_game_continues.assert_called_once_with(move=event.game.move_set.first())
    assert event.game.move_set.first().uci == "b10c8"
    assert event.game.move_set.count() == 1


@pytest.fixture
def mock_game_over(mocker):
    return mocker.patch.object(GameResult, "result", return_value=[0.5, 0.5])


@pytest.mark.django_db
def test_create_move_game_over(mock_game_over, event):
    assert event.game.move_set.count() == 0

    assert event.game.score1 == 0.0
    assert event.game.score2 == 0.0
    assert not event.game.finished_at

    HandleMove().perform(event=event)
    mock_game_over.assert_called_once_with(move=event.game.move_set.first())
    assert event.game.move_set.first().uci == "b10c8"
    assert event.game.move_set.count() == 1

    assert event.game.score1 == 0.5
    assert event.game.score2 == 0.5
    assert event.game.finished_at


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
        HandleMove().perform(event=event_with_non_player)
