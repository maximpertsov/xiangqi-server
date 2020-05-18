import json

from pytest import fixture, mark

from xiangqi.views import GameEventView
from rest_framework.test import force_authenticate


@fixture
def payload(game):
    return {
        "game": game.slug,
        "name": "move",
        "payload": {"fan": "a1a2", "fen": "FEN", "player": game.red_player.username},
    }


@fixture
def url():
    return "/api/game/events"


@fixture
def post(rf, url, payload):
    def wrapped(user):
        request = rf.post(
            url, data=json.dumps(payload), content_type="application/json"
        )
        force_authenticate(request, user)
        return GameEventView.as_view()(request)

    return wrapped


@mark.django_db
def test_create_move(post, game):
    assert game.move_set.count() == 0
    assert game.event_set.filter(name="move").count() == 0

    response = post(user=game.red_player)
    assert response.status_code == 201

    game.refresh_from_db()
    assert game.move_set.count() == 1
    assert game.event_set.filter(name="move").count() == 1
