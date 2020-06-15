from types import SimpleNamespace

import pytest
from rest_framework.test import force_authenticate

from xiangqi.models.color import Color
from xiangqi.queries.legal_moves import LegalMoves
from xiangqi.views import GameView


@pytest.fixture
def mocks(mocker):
    return SimpleNamespace(
        LegalMoves=mocker.patch.object(LegalMoves, "result", return_value={}),
        xiangqi=mocker.patch.multiple(
            "lib.pyffish.xiangqi",
            gives_check=mocker.MagicMock(return_value=False),
            start_fen=mocker.MagicMock(return_value="START_FEN"),
        ),
    )


@pytest.fixture
def get(rf, game, player):
    def wrapped():
        request = rf.get("/api/game")
        force_authenticate(request, user=player)
        return GameView.as_view()(request, slug=game.slug)

    return wrapped


@pytest.mark.django_db
def test_get_game_200(get, game, mocks):
    response = get()
    mocks.LegalMoves.assert_called_once_with(fen="START_FEN")
    assert response.status_code == 200
    assert response.data == {
        "slug": game.slug,
        "moves": [{"fen": "START_FEN", "gives_check": False, "legal_moves": {}}],
        "red_player": {"name": game.red_player.username, "color": Color.RED.value},
        "red_score": game.red_score,
        "black_player": {
            "name": game.black_player.username,
            "color": Color.BLACK.value,
        },
        "black_score": game.black_score,
        "open_draw_offer": None,
        "open_takeback_offer": None,
    }


@pytest.mark.django_db
def test_get_game_with_draw_offer(get, game, game_event_factory, mocks):
    game_event_factory(
        game=game, name="offered_draw", payload={"username": game.red_player.username}
    )
    game_event_factory(
        game=game, name="offered_draw", payload={"username": game.black_player.username}
    )

    response = get()
    assert response.status_code == 200
    assert response.data["open_draw_offer"] == game.red_player.username


@pytest.mark.django_db
def test_get_game_with_takeback_offer(get, game, game_event_factory, mocks):
    game_event_factory(
        game=game,
        name="offered_takeback",
        payload={"username": game.red_player.username},
    )

    response = get()
    assert response.status_code == 200
    assert response.data["open_takeback_offer"] == game.red_player.username
