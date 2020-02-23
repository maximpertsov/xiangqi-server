from unittest.mock import MagicMock, patch

import pytest

from xiangqi.queries.move import LegalMoves


@pytest.fixture
def fen():
    return 'rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w - - 0 1'


@pytest.fixture
def legal_moves():
    return ['e1e2']


def test_legal_moves(fen, legal_moves):
    with patch(
        'pyffish.legal_moves', MagicMock(return_value=legal_moves)
    ) as mock_get_legal_moves:
        assert LegalMoves(fen=fen).result() == legal_moves
        mock_get_legal_moves.assert_called_once_with('xiangqi', fen, [])
