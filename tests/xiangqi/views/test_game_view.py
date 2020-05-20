from pytest import fixture, mark

from xiangqi.queries.game_moves import GameMoves


@fixture
def url(game):
    return "/api/game/{}".format(game.slug)


@fixture
def get(client, url):
    def wrapped():
        return client.get(url)

    return wrapped


@fixture
def game_moves(mocker):
    return mocker.patch.object(GameMoves, "result", return_value=[])


@mark.django_db
def test_get_game_404(client):
    response = client.get("/api/game/FAKEGAME")
    assert response.status_code == 404


@mark.django_db
def test_get_game_200(get, game, game_moves):
    response = get()
    assert response.status_code == 200

    assert response.json() == {
        "moves": [],
        "players": [
            {"name": game.red_player.username, "color": "red"},
            {"name": game.black_player.username, "color": "black"},
        ],
    }
