import json

import pytest
from rest_framework.test import APIClient

from xiangqi.models import Game, GameRequest


@pytest.fixture
def players(player_factory):
    return player_factory.create_batch(2)


@pytest.fixture
def api_client(player):
    return APIClient()


@pytest.fixture
def api_call(api_client):
    def wrapped(user, http_method, url, payload=None):
        api_client.force_authenticate(user)

        args = [url]
        kwargs = (
            {"data": json.dumps(payload), "content_type": "application/json"}
            if payload
            else {}
        )

        return getattr(api_client, http_method)(*args, **kwargs)

    return wrapped


@pytest.mark.django_db
def test_create_game_request(players, api_call):
    assert not GameRequest.objects.exists()

    player, _ = players
    response = api_call(
        player,
        "post",
        "/api/game/request",
        payload={"player1": player.username, "parameters": {}},
    )
    assert response.status_code == 201

    game_request = GameRequest.objects.first()
    assert game_request.player1 == player
    assert game_request.player2 is None
    assert game_request.parameters == {}


@pytest.fixture
def patch(api_client, player_factory):
    def wrapped(game_request):
        payload = {"player2": player_factory().username}
        return api_client.patch(
            "/api/game/request/{}".format(game_request.pk),
            data=json.dumps(payload),
            content_type="application/json",
        )

    return wrapped


@pytest.mark.django_db
@pytest.mark.skip
def test_update_game_request_201(post, patch):
    post()
    game_request = GameRequest.objects.first()

    assert game_request.player2 is None
    assert Game.objects.count() == 0
    response = patch(game_request)
    assert response.status_code == 200
    game_request.refresh_from_db()
    assert game_request.player2 is not None
    assert Game.objects.count() == 1
