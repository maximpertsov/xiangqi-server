import json

import pytest


@pytest.fixture
def game_with_players(game, participant_factory, player_factory):
    p1, p2 = player_factory.create_batch(2)
    participant_factory(game=game, player=p1, color="red")
    participant_factory(game=game, player=p2, color="black")
    return game


@pytest.fixture
def red_player(game_with_players):
    return game_with_players.participant_set.get(color="red").player


@pytest.fixture
def payload(red_player):
    return {"name": "move", "player": red_player.user.username, "move": "a1a2"}


@pytest.fixture
def url(game_with_players):
    return "/api/game/{}/events".format(game_with_players.slug)


@pytest.fixture
def post_response(client, url, payload):
    return client.post(url, data=json.dumps(payload), content_type="application/json")


@pytest.mark.django_db
def test_create_move(response, game_with_players):
    assert response.status_code == 201
    assert response.json() == {}
    assert game_with_players.move_set.count() == 1