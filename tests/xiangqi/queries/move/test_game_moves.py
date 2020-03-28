import pytest

from xiangqi.queries.move.game_moves import GameMoves


@pytest.fixture
def game_with_moves(game, participant_factory, move_factory, player_factory):
    p1, p2 = player_factory.create_batch(2)
    participant1 = participant_factory(game=game, player=p1, color="red")
    participant2 = participant_factory(game=game, player=p2, color="black")
    move_factory(game=game, participant=participant1, name="a1a3")
    move_factory(game=game, participant=participant2, name="a10a9")
    move_factory(game=game, participant=participant1, name="i1i3")
    return game


@pytest.mark.django_db
def test_game_moves(game_with_moves):
    result = GameMoves(game_with_moves).result()
    assert len(result) == 4
    for serialized in result:
        assert "fen" in serialized
        assert "legal_moves" in serialized
        assert "gives_check" in serialized
        assert "move" in serialized
