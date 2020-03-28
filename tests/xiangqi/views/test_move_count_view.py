import pytest


@pytest.fixture
def game_with_moves(game, participant_factory, move_factory, player_factory):
    p1, p2 = player_factory.create_batch(2)
    participant1 = participant_factory(game=game, player=p1, color="red")
    participant2 = participant_factory(game=game, player=p2, color="black")
    move_factory(game=game, participant=participant1, name="a1a3")
    move_factory(game=game, participant=participant2, name="a10a9")
    move_factory(game=game, participant=participant1, name="i1i3")
    return game


@pytest.fixture
def get_response(client, game_with_moves):
    def wrapped():
        return client.get("/api/game/{}/move-count".format(game_with_moves.slug))

    return wrapped


@pytest.mark.django_db
def test_successful_response(get_response):
    response = get_response()
    assert response.status_code == 200
    assert response.json() == {"move_count": 3}


@pytest.mark.django_db
def test_only_count_moves_in_selected_game(get_response, move_factory):
    move_factory(name="a1a3")

    response = get_response()
    assert response.status_code == 200
    assert response.json() == {"move_count": 3}
