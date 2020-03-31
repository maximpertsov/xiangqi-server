import json

import pytest


@pytest.fixture
def game_with_players(game, participant_factory, move_factory, player_factory):
    p1, p2 = player_factory.create_batch(2)
    participant_factory(game=game, player=p1, color="red")
    participant_factory(game=game, player=p2, color="black")
    return game


@pytest.fixture
def red_player(game_with_players):
    return game_with_players.participant_set.get(color="red").player


@pytest.fixture
def black_player(game_with_players):
    return game_with_players.participant_set.get(color="black").player


@pytest.fixture
def poll(client, game_with_players):
    def wrapped():
        return client.get("/api/game/{}/poll".format(game_with_players.slug))

    return wrapped


@pytest.fixture
def make_move(client, game_with_players):
    def wrapped(move, player):
        payload = {"name": "move", "move": move, "player": player.user.username}
        return client.post(
            "/api/game/{}/events".format(game_with_players.slug),
            data=json.dumps(payload),
            content_type="application/json",
        )

    return wrapped


@pytest.mark.django_db
def test_successful_response(poll, make_move, red_player, black_player):
    response = poll()
    assert response.status_code == 200
    assert response.json() == {"update_count": 0}

    make_move("a1a3", red_player)
    response = poll()
    assert response.status_code == 200
    assert response.json() == {"update_count": 1}

    make_move("a10a9", black_player)
    response = poll()
    assert response.status_code == 200
    assert response.json() == {"update_count": 2}
