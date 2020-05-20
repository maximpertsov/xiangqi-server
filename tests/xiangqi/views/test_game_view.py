from pytest import fixture, mark
from rest_framework.test import force_authenticate

from xiangqi.views import GameView


@fixture
def get(rf, game, player):
    def wrapped():
        request = rf.get("/api/game")
        force_authenticate(request, user=player)
        return GameView.as_view()(request, slug=game.slug)

    return wrapped


@mark.django_db
def test_get_game_200(get, game):
    response = get()
    assert response.status_code == 200

    assert response.data == {
        "moves": [],
        "players": [
            {"name": game.red_player.username, "color": "red"},
            {"name": game.black_player.username, "color": "black"},
        ],
    }
