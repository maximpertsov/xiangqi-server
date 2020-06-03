import json

import pytest
from rest_framework.test import force_authenticate

from xiangqi.queries.game_result import GameResult
from xiangqi.views import GameEventView


@pytest.fixture
def mocks(mocker):
    mocker.patch.object(
        GameResult, "result", new_callable=mocker.PropertyMock, return_value=[0, 0]
    )


@pytest.fixture
def payload(game):
    return {
        "game": game.slug,
        "name": "move",
        "payload": {"uci": "a1a2", "fen": "FEN", "player": game.red_player.username},
    }


@pytest.fixture
def post(rf, payload):
    def wrapped(user):
        request = rf.post(
            "/api/game/events",
            data=json.dumps(payload),
            content_type="application/json",
        )
        force_authenticate(request, user)
        return GameEventView.as_view()(request)

    return wrapped


@pytest.mark.django_db
def test_create_move(mocks, post, game):
    assert game.move_set.count() == 0
    assert game.event_set.filter(name="move").count() == 0

    response = post(user=game.red_player)
    assert response.status_code == 201

    game.refresh_from_db()
    assert game.move_set.count() == 1
    assert game.event_set.filter(name="move").count() == 1
