from unittest.mock import MagicMock, patch

import pytest

from xiangqi.queries.move.legal_moves import LegalMoves


@pytest.fixture
def fen():
    return 'rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w - - 0 1'


@pytest.fixture
def moves():
    return []


@pytest.fixture
def legal_moves():
    return ['e1e2']


def test_legal_moves(fen, moves, legal_moves):
    with patch(
        'pyffish.legal_moves', MagicMock(return_value=legal_moves)
    ) as mock_get_legal_moves:
        assert LegalMoves(fen=fen, moves=moves).result() == legal_moves
        mock_get_legal_moves.assert_called_once_with('xiangqi', fen, moves)
