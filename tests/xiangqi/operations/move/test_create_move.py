import pytest
from pytest_factoryboy import register

from tests import factories

register(factories.UserFactory)
register(factories.PlayerFactory)
register(factories.GameFactory)
register(factories.MoveFactory)
register(factories.ParticipantFactory)


@pytest.mark.django_db
@pytest.mark.skip("TODO")
def test_create_move(client, game_with_players, pieces):
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
