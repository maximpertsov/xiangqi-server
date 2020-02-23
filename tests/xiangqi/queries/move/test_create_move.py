from unittest.mock import MagicMock, patch

import pytest

from xiangqi.queries.move.create_move import CreateMove
from xiangqi.queries.move.legal_moves import LegalMoves


@pytest.fixture
def fen():
    return 'FEN 0'


@pytest.fixture
def new_fen():
    return 'FEN 1'


@pytest.fixture
def move():
    return 'MOVE'


@pytest.fixture
def new_legal_moves():
    return []


@pytest.fixture
def new_move(move, new_fen, new_legal_moves):
    return {'fen': new_fen, 'move': move, 'legal_moves': new_legal_moves}


def test_create_move(move, new_fen, new_move):
    with patch(
        'pyffish.get_fen', MagicMock(return_value=new_fen)
    ) as mock_get_fen, patch.object(
        LegalMoves, 'result', return_value=new_legal_moves,
    ) as mock_query_legal_moves:
        assert CreateMove(fen=fen, move=move).result() == new_move
        mock_get_fen.assert_called_once_with('xiangqi', fen, [move])
        mock_query_legal_moves.assert_called_once_with(fen=fen, moves=[move])
