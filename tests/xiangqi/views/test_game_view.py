import pytest
from rest_framework.test import force_authenticate

from xiangqi.views import GameView


@pytest.fixture
def mock_pyffish(mocker):
    return mocker.patch.multiple(
        "lib.pyffish.xiangqi",
        gives_check=mocker.MagicMock(return_value=False),
        start_fen=mocker.MagicMock(return_value="START_FEN"),
        legal_moves=mocker.MagicMock(return_value=[]),
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
        "moves": [{"fen": "START_FEN", "gives_check": False, "legal_moves": {}}],
        "players": [
            {"name": game.red_player.username, "color": "red"},
            {"name": game.black_player.username, "color": "black"},
        ],
    }
