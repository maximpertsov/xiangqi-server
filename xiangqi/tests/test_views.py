import pytest
from pytest_factoryboy import register

from xiangqi.tests import factories

register(factories.UserFactory)
register(factories.PlayerFactory)
register(factories.GameFactory)


@pytest.mark.django_db
def test_get_game(client, game):
    r = client.get('/api/game/0')
    assert r.status_code == 404

    r = client.get('/api/game/{}'.format(game.pk))
    assert r.status_code == 200
