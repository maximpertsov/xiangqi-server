import json

import pytest
from django.core.management import call_command
from pytest_factoryboy import register

from tests import factories

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
    assert data['players'] == []


@pytest.mark.django_db
def test_get_game_pieces(client, game, pieces):
    r = client.get('/api/game/{}'.format(game.slug))
    assert r.status_code == 200

    data = r.json()

    expected_fen = 'rheakaehr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RHEAKAEHR'
    assert data['initial_fen'] == expected_fen
    assert data['players'] == []


@pytest.mark.django_db
def test_get_games_for_non_participant(client, game_with_players):
    url = '/api/player/{}/games'.format('FAKE')
    r = client.get(url)
    assert r.status_code == 200

    data = r.json()
    assert data['games'] == []


@pytest.mark.django_db
def test_get_games_for_participant(client, game_with_players):
    username = game_with_players.participant_set.first().player.user.username
    url = '/api/player/{}/games'.format(username)
    r = client.get(url)
    assert r.status_code == 200

    data = r.json()
    assert data['games'] == [{'slug': game_with_players.slug}]


@pytest.mark.django_db
def test_post_move_201_then_get(client, game_with_players, pieces):
    participant = game_with_players.participant_set.first()
    url = '/api/game/{}/moves'.format(game_with_players.slug)
    data = {
        "player": "{}".format(participant.player.user.username),
        "from": [0, 1],
        "to": [2, 2],
        "type": "move",
    }
    r = client.post(url, data=json.dumps(data), content_type="application/json")
    assert r.status_code == 201

    r = client.get(url)
    assert r.status_code == 200
    data = r.json()
    assert len(data['moves']) == 1

    # TODO: move to own unit test
    # Test move count api
    r = client.get('/api/game/{}/move-count'.format(game_with_players.slug))
    assert r.status_code == 200
    data = r.json()
    assert data['move_count'] == 1


@pytest.mark.django_db
@pytest.mark.skip('Requires cookies in request')
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


@pytest.mark.django_db
def test_login(client, user):
    password = 's0_s0_secure'
    user.set_password(password)
    user.save()

    assert user.accesstoken_set.count() == 0
    assert user.refreshtoken_set.count() == 0

    data = {'username': user.username, 'password': password}

    response = client.post(
        '/api/login', data=json.dumps(data), content_type="application/json"
    )
    assert response.status_code == 201

    cookies = response.client.cookies
    assert 'access_token' in cookies
    assert 'refresh_token' in cookies

    assert user.accesstoken_set.count() == 1
    assert user.refreshtoken_set.count() == 1
