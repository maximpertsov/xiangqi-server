from pytest import mark


@mark.django_db
def test_get_games_for_non_player(client, player_factory):
    non_player = player_factory(username="NON_ACTIVE_PLAYER")
    url = "/api/player/{}/games".format(non_player.username)
    response = client.get(url)
    assert response.status_code == 200

    assert response.json() == {"games": []}


@mark.django_db
def test_get_games_for_player(client, game):
    url = "/api/player/{}/games".format(game.red_player.username)
    response = client.get(url)
    assert response.status_code == 200

    assert response.json() == {"games": [{"slug": game.slug}]}
