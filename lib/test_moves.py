from math import ceil

import pytest

from fen import decode_fen, decode_fen2

RANKS = 10
FILES = 9

RED_PIECES = set('rheakp')
BLACK_PIECES = set(map(str.upper, RED_PIECES))


def get_slot(rank, file):
    return file + rank * FILES


def get_rank(slot):
    return ceil(slot / RANKS)


def get_file(slot):
    return slot % FILES


def get_rank_file(slot):
    return get_rank(slot), get_file(slot)


def empty(slots, slot):
    return slots[slot] is None


def in_bounds(slot):
    return 0 <= slot < RANKS * FILES


# Add move with generic checks
def _add(moves, slots, from_slot, to_slot):
    if not in_bounds(to_slot):
        return
    if from_slot == to_slot:
        return
    moves.add(to_slot)


# Assumes there is a piece on both s1 and s2
def same_color(slots, s1, s2):
    return (s1 in RED_PIECES and s2 in RED_PIECES) or (
        s1 in BLACK_PIECES and s2 in BLACK_PIECES
    )


# Assumes there is a piece on both s1 and s2
def diff_color(slots, s1, s2):
    return not same_color(slots, s1, s2)


# WIP
def legal_moves(slots, slot):
    code = slots[slot]
    rank, file = get_rank_file(slot)
    moves = set()
    if code in 'Pp':
        fwd = 1 if code == 'p' else -1  # Black moves down, so ranks go up
        _add(moves, slots, slot, get_slot(fwd + rank, file))
        # Pawn across river
        if (code == 'p' and rank > 4) or (code == 'P' and rank < 5):
            _add(moves, slots, slot, get_slot(rank, file + 1))
            _add(moves, slots, slot, get_slot(rank, file - 1))

    return moves


def main():
    # fen = '4kaR2/4a4/3hR4/7H1/9/9/9/9/4Ap1r1/3AK3c'
    # fen = 'rheakaehr/9/2c3c2/p1p1p1p1p/9/9/P1P1P1P1P/2C3C2/9/RHEAKAEHR'
    # fen = 'r7r/9/9/9/9/9/9/9/9/R7R'
    fen = '4k4/9/9/p1p1p1p1p/9/9/P1P1P1P1P/9/9/4K4'
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


def test_legal_pawn_moves():
    fen = '4k4/9/9/p1p1p1p1p/9/1p7/P1P1P1P1P/9/9/4K4'
    slots = decode_fen2(fen)
    assert legal_moves(slots, get_slot(3, 0)) == {get_slot(4, 0)}
    assert legal_moves(slots, get_slot(5, 1)) == {
        get_slot(6, 1), get_slot(5, 0), get_slot(5, 2)
    }


if __name__ == '__main__':
    main()
    pytest.main()
