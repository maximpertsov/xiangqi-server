import json

import pytest
from rest_framework.test import APIClient

from xiangqi.models import GameRequest


@pytest.fixture
def api_client(player):
    client = APIClient()
    client.force_authenticate(player)
    return client


@pytest.fixture
def post(api_client, player):
    def wrapped():
        payload = {"players": [player.username], "parameters": {}}
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
def join(api_client, player_factory):
    def wrapped(game_request):
        payload = {"gamerequest": game_request.pk, "player": player_factory().username}
        return api_client.post(
            "/api/game/requests/player",
            data=json.dumps(payload),
            content_type="application/json",
        )

    return wrapped


# TODO: post to through table
@pytest.mark.django_db
def test_update_game_request_201(post, join):
    post()
    game_request = GameRequest.objects.first()
    response = join(game_request)
    assert response.status_code == 201
    assert game_request.player_set.count() == 2
