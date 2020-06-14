import json
from types import SimpleNamespace

import pytest
from rest_framework.test import force_authenticate

from xiangqi.models import DrawEvent
from xiangqi.models.draw_event import DrawEventTypes
from xiangqi.models.takeback_event import TakebackEventTypes
from xiangqi.queries.game_result import GameResult
from xiangqi.views import GameEventView


@pytest.fixture
def mocks(mocker):
    return SimpleNamespace(
        GameResult=mocker.patch.object(GameResult, "result", return_value=[0, 0])
    )


@pytest.fixture
def post(rf):
    def wrapped(user, payload, expected_status_code=201):
        request = rf.post(
            "/api/game/events",
            data=json.dumps(payload),
            content_type="application/json",
        )
        force_authenticate(request, user)
        response = GameEventView.as_view()(request)
        assert response.status_code == expected_status_code
        return response

    return wrapped


@pytest.fixture
def around(game, event_name):
    assert game.event_set.filter(name=event_name).count() == 0
    yield
    assert game.event_set.filter(name=event_name).count() == 1


@pytest.mark.django_db
@pytest.mark.parametrize("event_name", ["move"])
def test_create_move(event_name, around, mocks, post, game):
    assert game.move_set.count() == 0

    post(
        user=game.red_player,
        payload={
            "game": game.slug,
            "name": event_name,
            "payload": {
                "uci": "a1a2",
                "fen": "FEN",
                "player": game.red_player.username,
            },
        },
    )

    assert game.move_set.count() == 1
    assert mocks.GameResult.called_once_with(move=game.move_set.first())


@pytest.mark.django_db
@pytest.mark.parametrize("event_name", [DrawEventTypes.OFFERED_DRAW.value])
def test_offer_draw(event_name, around, post, game):
    DrawEvent.open_offers.filter(game=game).count == 0

    post(
        user=game.red_player,
        payload={"game": game.slug, "name": event_name, "payload": {}},
    )

    DrawEvent.open_offers.filter(game=game).count == 1


@pytest.mark.django_db
@pytest.mark.parametrize("event_name", [DrawEventTypes.ACCEPTED_DRAW.value])
def test_accepted_draw(event_name, around, post, game):
    assert game.red_score == 0.0
    assert game.black_score == 0.0
    assert not game.finished_at

    post(
        user=game.red_player,
        payload={
            "game": game.slug,
            "name": event_name,
            "payload": {"username": game.red_player.username},
        },
    )

    game.refresh_from_db()
    assert game.red_score == 0.5
    assert game.black_score == 0.5
    assert game.finished_at


@pytest.mark.django_db
@pytest.mark.parametrize("event_name", ["resigned"])
def test_resigned(event_name, around, post, game):
    assert game.red_score == 0.0
    assert game.black_score == 0.0
    assert not game.finished_at

    post(
        user=game.red_player,
        payload={
            "game": game.slug,
            "name": event_name,
            "payload": {"username": game.red_player.username},
        },
    )

    game.refresh_from_db()
    assert game.red_score == 0.0
    assert game.black_score == 1.0
    assert game.finished_at


@pytest.mark.django_db
@pytest.mark.parametrize("event_name", [TakebackEventTypes.ACCEPTED_TAKEBACK.value])
def test_takeback_accepted(
    event_name, around, post, game, move_factory, game_event_factory
):
    move1 = move_factory(game=game, player=game.red_player)
    move2 = move_factory(game=game, player=game.black_player)
    game_event_factory(
        game=game,
        name=TakebackEventTypes.OFFERED_TAKEBACK.value,
        payload={"username": game.black_player.username},
    )
    move3 = move_factory(game=game, player=game.red_player)
    assert set(game.move_set.all()) == ([move1, move2, move3])

    post(
        user=game.red_player,
        payload={
            "game": game.slug,
            "name": event_name,
            "payload": {"username": game.red_player.username},
        },
    )

    assert set(game.move_set.all()) == ([move1])
