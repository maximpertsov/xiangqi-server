import pytest

from xiangqi.queries.game_players import GamePlayers


@pytest.mark.django_db
def test_game_players(game):
    assert GamePlayers(game=game).result() == [
        {"name": "rosie", "color": "red"},
        {"name": "bob", "color": "black"},
    ]
