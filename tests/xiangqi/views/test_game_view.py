from pytest import fixture, mark


@fixture
def url(game):
    return "/api/game/{}".format(game.slug)


@fixture
def get(client, url):
    def wrapped():
        return client.get(url)

    return wrapped


@mark.django_db
def test_get_game_404(client):
    response = client.get("/api/game/FAKEGAME")
    assert response.status_code == 404


@mark.django_db
def test_get_game_200(get, game):
    response = get()
    assert response.status_code == 200
    assert response.json() == {
        "players": [
            {"name": game.red_player.username, "color": "red"},
            {"name": game.black_player.username, "color": "black"},
        ]
    }
