from lib.pyffish import xiangqi
from xiangqi.queries.move_order import MoveOrder


def test_first_move():
    fen = xiangqi.start_fen()
    assert MoveOrder(fen=fen).result == 1


def test_second_move():
    fen = xiangqi.get_fen(xiangqi.start_fen(), ["a1a2"])
    assert MoveOrder(fen=fen).result == 2
