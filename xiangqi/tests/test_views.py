import json

import pytest
from django.core.management import call_command
from pytest_factoryboy import register

from xiangqi.tests import factories

register(factories.UserFactory)
register(factories.PlayerFactory)
register(factories.GameFactory)
register(factories.MoveFactory)
register(factories.ParticipantFactory)


@pytest.fixture
def pieces(game):
    call_command('loaddata', 'pieces.json')
    return game


@pytest.fixture
def game_with_players(game, participant_factory, player_factory):
    p1, p2 = player_factory.create_batch(2)
    participant_factory(game=game, player=p1, color='red')
    participant_factory(game=game, player=p2, color='black')
    return game


@pytest.mark.django_db
def test_get_game_404(client):
    r = client.get('/api/game/FAKEGAME')
    assert r.status_code == 404


@pytest.mark.django_db
def test_get_game_200(client, game):
    r = client.get('/api/game/{}'.format(game.slug))
    assert r.status_code == 200

    data = r.json()
    assert data['initial_fen'] == '9/9/9/9/9/9/9/9/9/9'
    assert data['ranks'] == 10
    assert data['files'] == 9
    assert data['players'] == []


@pytest.mark.django_db
def test_get_game_pieces(client, game, pieces):
    r = client.get('/api/game/{}'.format(game.slug))
    assert r.status_code == 200

    data = r.json()
    assert (
        data['initial_fen']
        == 'rheakaehr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RHEAKAEHR'
    )
    assert data['ranks'] == 10
    assert data['files'] == 9
    assert data['players'] == []


@pytest.mark.django_db
def test_post_move_201_then_get(client, game_with_players, pieces):
    participant = game_with_players.participant_set.first()
    url = '/api/game/{}/moves'.format(game_with_players.slug)
    data = {
        "player": "{}".format(participant.player.user.username),
        "piece": "h",
        "from": [0, 1],
        "to": [2, 2],
        "type": "move",
    }
    r = client.post(url, data=json.dumps(data), content_type="application/json")
    assert r.status_code == 201

    r = client.get(url)
    r.status_code == 200
    data = r.json()
    assert len(data['moves']) == 1


@pytest.mark.django_db
def test_authenticate(client, user):
    password = 's0_s0_secure'
    user.set_password(password)
    user.save()

    data = {'username': user.username, 'password': password}

    r = client.post(
        '/api/authenticate', data=json.dumps(data), content_type="application/json"
    )
    assert r.status_code == 201
    response_data = r.json()
    assert 'access_token' in response_data
