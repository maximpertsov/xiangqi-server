import json

import pytest
from rest_framework.test import APIClient

from xiangqi.models import Game, GameRequest


@pytest.fixture
def api_client(player):
    client = APIClient()
    client.force_authenticate(player)
    return client


@pytest.fixture
def post(api_client, player):
    def wrapped():
        payload = {"player1": player.username, "parameters": {}}
        return api_client.post(
            "/api/game/requests",
            data=json.dumps(payload),
            content_type="application/json",
        )

    return wrapped


@pytest.mark.django_db
def test_create_game_request_201(post):
    GameRequest.objects.count == 0
    response = post()
    assert response.status_code == 201
    GameRequest.objects.count == 1


@pytest.fixture
def patch(api_client, player_factory):
    def wrapped(game_request):
        payload = {"player2": player_factory().username}
        return api_client.patch(
            "/api/game/requests/{}".format(game_request.pk),
            data=json.dumps(payload),
            content_type="application/json",
        )

    return wrapped


@pytest.mark.django_db
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
