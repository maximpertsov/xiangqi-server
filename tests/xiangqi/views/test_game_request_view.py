import json
from collections import OrderedDict

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


@pytest.mark.django_db
def test_create_game_request(players, api_call):
    assert not GameRequest.objects.exists()

    player, _ = players
    response = api_call(
        "post",
        "/api/game/request",
        payload={"player1": player.username, "parameters": {}},
        user=player,
    )
    assert response.status_code == 201

    game_request = GameRequest.objects.first()
    assert game_request.player1 == player
    assert game_request.player2 is None
    assert game_request.parameters == {}


@pytest.mark.django_db
def test_accept_game_request(players, game_request_factory, api_call):
    player1, player2 = players
    game_request = game_request_factory(player1=player1)

    assert game_request.player2 is None
    assert Game.objects.count() == 0

    response = api_call(
        "patch",
        f"/api/game/request/{game_request.pk}",
        payload={"player2": player2.username},
        user=player2,
    )
    assert response.status_code == 200
    game_request.refresh_from_db()
    assert game_request.player2 == player2
    assert Game.objects.count() == 1

    # TODO: add logic for which side each player is on
    # game = Game.objects.first()
    # assert game.player1 == player1
    # assert game.player2 == player2


@pytest.mark.django_db
def test_reject_game_request(players, game_request_factory, api_call):
    player1, player2 = players
    game_request = game_request_factory(player1=player1)

    response = api_call("delete", f"/api/game/request/{game_request.pk}", user=player2)
    assert response.status_code == 204
    with pytest.raises(GameRequest.DoesNotExist):
        game_request.refresh_from_db()


@pytest.mark.django_db
def test_list_game_requests(players, game_request_factory, api_call):
    player1, player2 = players
    open_game_request = game_request_factory(player1=player1)
    game_request_factory(player1=player1, player2=player2)

    response = api_call("get", "/api/game/request", user=player2)
    assert response.status_code == 200

    assert response.data == [
        OrderedDict(
            {
                "id": open_game_request.pk,
                "player1": player1.username,
                "player2": None,  # TODO: remove this?
                "parameters": open_game_request.parameters,
            }
        )
    ]
