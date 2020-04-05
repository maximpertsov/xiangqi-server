import pytest

from xiangqi.queries.move.game_moves import GameMoves


@pytest.fixture
def game_with_moves(game_factory, move_factory, player_factory):
    red_player, black_player = player_factory.create_batch(2)
    game = game_factory(red_player=red_player, black_player=black_player)
    move_factory(game=game, player=red_player, name="a1a3")
    move_factory(game=game, player=black_player, name="a10a9")
    move_factory(game=game, player=red_player, name="i1i3")
    return game


@pytest.mark.django_db
def test_game_moves(game_with_moves):
    result = GameMoves(game=game_with_moves).result()
    assert len(result) == 4
    for index, serialized in enumerate(result):
        assert "fen" in serialized
        assert "legal_moves" in serialized
        assert "gives_check" in serialized
        assert "move" in serialized

        if index == 0:
            assert serialized['player'] is None
        elif index % 2 == 1:
            assert serialized['player']['color'] == 'red'
        else:
            assert serialized['player']['color'] == 'black'
