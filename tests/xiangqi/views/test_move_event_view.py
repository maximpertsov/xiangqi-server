import json

from pytest import fixture, mark


@fixture
def payload(game):
    return {"name": "move", "player": game.red_player.username, "move": "a1a2"}


@fixture
def url(game):
    return "/api/game/{}/events".format(game.slug)


@fixture
def post(client, url, payload):
    def wrapped():
        return client.post(
            url, data=json.dumps(payload), content_type="application/json"
        )

    return wrapped


@mark.django_db
def test_create_move(post, game):
    assert game.move_set.count() == 0
    assert game.event_set.filter(name="move").count() == 0

    response = post()
    assert response.status_code == 201
    assert response.json() == {}

    game.refresh_from_db()
    assert game.move_set.count() == 1
    assert game.event_set.filter(name="move").count() == 1
