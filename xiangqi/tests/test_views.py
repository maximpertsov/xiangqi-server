import pytest
from django.core.management import call_command
from pytest_factoryboy import register

from xiangqi.tests import factories

register(factories.UserFactory)
register(factories.PlayerFactory)
register(factories.GameFactory)


@pytest.mark.django_db
def test_get_game_404(client):
    r = client.get('/api/game/0')
    assert r.status_code == 404


@pytest.mark.django_db
def test_get_game_200(client, game):
    r = client.get('/api/game/{}'.format(game.pk))
    assert r.status_code == 200

    data = r.json()
    assert data['fen'] == '9/9/9/9/9/9/9/9/9/9'
    assert data['ranks'] == 10
    assert data['files'] == 9
    assert data['players'] == []


@pytest.mark.django_db
def test_get_game_pieces(django_db_blocker, client, game):
    call_command('loaddata', 'pieces.json')

    r = client.get('/api/game/{}'.format(game.pk))
    assert r.status_code == 200

    data = r.json()
    assert data['fen'] == 'rheakaehr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RHEAKAEHR'
    assert data['ranks'] == 10
    assert data['files'] == 9
    assert data['players'] == []
