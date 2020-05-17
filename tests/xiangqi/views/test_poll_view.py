import json

from pytest import fixture, mark


@fixture
def poll(client, game):
    def wrapped():
        return client.get("/api/game/{}/poll".format(game.slug))

    return wrapped


@fixture
def make_move(client, game):
    def wrapped(fan, player):
        payload = {"name": "move", "fan": fan, "player": player.username}
        return client.post(
            "/api/game/{}/events".format(game.slug),
            data=json.dumps(payload),
            content_type="application/json",
        )

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
