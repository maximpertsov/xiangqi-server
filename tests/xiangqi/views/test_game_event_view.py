import json
from types import SimpleNamespace

import pytest
from rest_framework.test import force_authenticate

from xiangqi.models.draw_event import DrawEventTypes
from xiangqi.queries.game_result import GameResult
from xiangqi.views import GameEventView


@pytest.fixture
def mocks(mocker):
    return SimpleNamespace(
        GameResult=mocker.patch.object(GameResult, "result", return_value=[0, 0])
    )


@pytest.fixture
def post(rf):
    def wrapped(user, payload):
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
    event_name = "move"

    assert game.move_set.count() == 0
    assert game.event_set.filter(name=event_name).count() == 0

    payload = {
        "game": game.slug,
        "name": event_name,
        "payload": {"uci": "a1a2", "fen": "FEN", "player": game.red_player.username},
    }
    response = post(user=game.red_player, payload=payload)
    assert response.status_code == 201

    assert mocks.GameResult.called_once_with(move=game.move_set.first())
    assert game.move_set.count() == 1
    assert game.event_set.filter(name=event_name).count() == 1


@pytest.mark.django_db
def test_offer_draw(post, game):
    event_name = DrawEventTypes.OFFERED_DRAW.value

    assert game.event_set.filter(name=event_name).count() == 0

    payload = {"game": game.slug, "name": event_name, "payload": {}}
    response = post(user=game.red_player, payload=payload)
    assert response.status_code == 201

    assert game.event_set.filter(name=event_name).count() == 1


@pytest.mark.django_db
def test_accepted_draw(post, game):
    event_name = DrawEventTypes.ACCEPTED_DRAW.value

    assert game.event_set.filter(name=event_name).count() == 0

    payload = {"game": game.slug, "name": event_name, "payload": {}}
    response = post(user=game.red_player, payload=payload)
    assert response.status_code == 201

    assert game.event_set.filter(name=event_name).count() == 1

    game.refresh_from_db()
    assert game.red_score == 0.5
    assert game.black_score == 0.5
    assert game.finished_at
