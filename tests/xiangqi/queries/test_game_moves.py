import pytest

from xiangqi.queries.game_moves import GameMoves


@pytest.fixture
def game_with_moves(game, move_factory):
    move_factory(game=game, player=game.red_player, fan="a1a3")
    move_factory(game=game, player=game.black_player, fan="a10a9")
    move_factory(game=game, player=game.red_player, fan="i1i3")
    return game


@pytest.mark.django_db
def test_game_moves(game_with_moves):
    result = GameMoves(game=game_with_moves).result()
    assert len(result) == 4
    for index, serialized in enumerate(result):
        assert "fen" in serialized
        assert "legal_moves" in serialized
        assert "gives_check" in serialized
        assert "fan" in serialized

        if index == 0:
            assert serialized["player_name"] is None
        elif index % 2 == 1:
            assert serialized["player_name"] == "rosie"
        else:
            assert serialized["player_name"] == "bob"
