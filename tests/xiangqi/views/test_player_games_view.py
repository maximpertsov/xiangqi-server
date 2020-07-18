import json

import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client(player):
    return APIClient()


@pytest.fixture
def call_api(api_client):
    def wrapped(http_method, url, user=None, payload=None):
        api_client.force_authenticate(user)

        args = [url]
        kwargs = (
            {"data": json.dumps(payload), "content_type": "application/json"}
            if payload
            else {}
        )

        return getattr(api_client, http_method)(*args, **kwargs)

    return wrapped


# @pytest.mark.django_db
# def test_get_games_for_non_player(client, player_factory):
#     non_player = player_factory(username="NON_ACTIVE_PLAYER")
#     url = "/api/player/{}/games".format(non_player.username)
#     response = client.get(url)
#     assert response.status_code == 200
#
#     assert response.json() == {"games": []}


@pytest.mark.django_db
def test_get_games_for_player(call_api, game):
    url = "/api/player/{}/games".format(game.player1.username)
    response = call_api("get", url, user=game.player1)
    assert response.status_code == 200

    data = response.json()
    assert data["games"][0]["slug"] == game.slug
