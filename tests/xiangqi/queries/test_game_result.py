from lib.pyffish import xiangqi
from xiangqi.queries.game_result import GameResult


def test_no_result():
    fen = xiangqi.start_fen()
    assert GameResult(fen=fen).result == [0, 0]


def test_red_wins():
    fen = "4k4/9/9/9/9/9/9/9/9/3RRK3 b"
    assert GameResult(fen=fen).result == [1, 0]


def test_black_wins():
    fen = "3krr3/9/9/9/9/9/9/9/9/4K4 w"
    assert GameResult(fen=fen).result == [0, 1]


def test_draw_by_insufficient_material():
    fen = "3k5/9/9/9/9/9/9/9/9/5K3 w"
    assert GameResult(fen=fen).result == [0.5, 0.5]
