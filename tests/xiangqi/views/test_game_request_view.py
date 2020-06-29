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
        payload = {"player": player.username, "parameters": {}}
        return api_client.post(
            "/api/game/requests",
            data=json.dumps(payload),
            content_type="application/json",
        )

    return wrapped


@pytest.mark.django_db
def test_create_request_201(post):
    GameRequest.objects.count == 0
    response = post()
    assert response.status_code == 201
    GameRequest.objects.count == 1
