import pytest


@pytest.mark.django_db
def test_get_game(client):
    r = client.get('/api/game/2')
    assert r.status_code == 404
