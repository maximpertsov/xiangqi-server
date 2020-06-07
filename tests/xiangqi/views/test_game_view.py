import pytest
from rest_framework.test import force_authenticate

from xiangqi.models.color import Color
from xiangqi.queries.game_result import GameResult
from xiangqi.queries.legal_moves import LegalMoves
from xiangqi.views import GameView


@pytest.fixture
def mock_pyffish(mocker):
    mocker.patch.object(
        GameResult, "result", new_callable=mocker.PropertyMock, return_value=[0, 0]
    )
    mocker.patch.object(
        LegalMoves, "result", new_callable=mocker.PropertyMock, return_value={}
    )
    mocker.patch.multiple(
        "lib.pyffish.xiangqi",
        gives_check=mocker.MagicMock(return_value=False),
        start_fen=mocker.MagicMock(return_value="START_FEN"),
    )


@pytest.fixture
def get(rf, game, player):
    def wrapped():
        request = rf.get("/api/game")
        force_authenticate(request, user=player)
        return GameView.as_view()(request, slug=game.slug)

    return wrapped


@pytest.mark.django_db
def test_get_game_200(get, game, mock_pyffish):
    response = get()
    assert response.status_code == 200

    assert response.data == {
        "slug": game.slug,
        "moves": [
            {
                "fen": "START_FEN",
                "gives_check": False,
                "legal_moves": {},
                "game_result": [0, 0],
            }
        ],
        "red_player": {"name": game.red_player.username, "color": Color.RED.value},
        "red_score": game.red_score,
        "black_player": {
            "name": game.black_player.username,
            "color": Color.BLACK.value,
        },
        "black_score": game.black_score,
        "open_draw_offer": None,
    }


@pytest.mark.django_db
def test_get_game_with_draw_offer(get, game, game_event_factory, mock_pyffish):
    game_event_factory(
        game=game, name="offered_draw", payload={"username": game.red_player.username}
    )
    game_event_factory(
        game=game, name="offered_draw", payload={"username": game.black_player.username}
    )

    response = get()
    assert response.status_code == 200

    assert response.data["open_draw_offer"] == game.red_player.username
