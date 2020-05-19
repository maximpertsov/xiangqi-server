import json

from pytest import fixture, mark
from rest_framework.test import force_authenticate

from xiangqi.views import GameEventView


@fixture
def payload(game):
    return {
        "game": game.slug,
        "name": "move",
        "payload": {"fan": "a1a2", "fen": "FEN", "player": game.red_player.username},
    }


@fixture
def poll(client, game):
    def wrapped():
        return client.get("/api/game/{}/poll".format(game.slug))

    return wrapped


@fixture
def make_move(rf, payload):
    def wrapped(fan, player):
        request = rf.post(
            "/api/game/events",
            data=json.dumps(payload),
            content_type="application/json",
        )
        force_authenticate(request, user=player)
        return GameEventView.as_view()(request)

    return wrapped


@mark.django_db
def test_successful_response(poll, make_move, game):
    response = poll()
    assert response.status_code == 200
    assert response.json() == {"update_count": 0}

    make_move("a1a3", game.red_player)
    response = poll()
    assert response.status_code == 200
    assert response.json() == {"update_count": 1}

    make_move("a10a9", game.black_player)
    response = poll()
    assert response.status_code == 200
    assert response.json() == {"update_count": 2}
