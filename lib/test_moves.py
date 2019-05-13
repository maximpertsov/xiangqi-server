import pytest
from math import ceil

from fen import decode_fen

RANKS = 10
FILES = 9


def get_slot(rank, file):
    return file + rank * FILES


def get_rank(slot):
    return ceil(slot / RANKS)


def get_file(slot):
    return slot % FILES


def main():
    # fen = '4kaR2/4a4/3hR4/7H1/9/9/9/9/4Ap1r1/3AK3c'
    fen = 'rheakaehr/9/2c3c2/p1p1p1p1p/9/9/P1P1P1P1P/2C3C2/9/RHEAKAEHR'
    print(decode_fen(fen))


# Tests
def test_get_slot():
    assert get_slot(0, 0) == 0
    assert get_slot(5, 3) == 48


def test_get_rank():
    assert get_rank(0) == 0
    assert get_rank(48) == 5


def test_get_file():
    assert get_file(0) == 0
    assert get_file(48) == 3


if __name__ == '__main__':
    main()
    pytest.main()
