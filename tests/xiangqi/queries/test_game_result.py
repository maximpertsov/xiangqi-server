import pytest

from lib.pyffish import xiangqi
from xiangqi.models.draw_event import DrawEventTypes
from xiangqi.queries.game_result import GameResult


@pytest.mark.django_db
def test_no_result(move_factory):
    move = move_factory(fen=xiangqi.start_fen())
    assert GameResult(move=move).result == [0, 0]


@pytest.mark.django_db
def test_red_wins(move_factory):
    move = move_factory(fen="4k4/9/9/9/9/9/9/9/9/3RRK3 b")
    assert GameResult(move=move).result == [1, 0]


@pytest.mark.django_db
def test_black_wins(move_factory):
    move = move_factory(fen="3krr3/9/9/9/9/9/9/9/9/4K4 w")
    assert GameResult(move=move).result == [0, 1]


@pytest.mark.django_db
def test_draw_by_insufficient_material(move_factory):
    move = move_factory(fen="3k5/9/9/9/9/9/9/9/9/5K3 w")
    assert GameResult(move=move).result == [0.5, 0.5]


@pytest.mark.django_db
def test_draw_by_accepted_draw(game_event_factory, move_factory):
    move = move_factory(fen=xiangqi.start_fen())
    game_event_factory(game=move.game, name=DrawEventTypes.ACCEPTED_DRAW.value)
    assert GameResult(move=move).result == [0.5, 0.5]
