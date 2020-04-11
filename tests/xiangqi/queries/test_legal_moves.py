import pytest

from xiangqi.queries.legal_moves import LegalMoves


@pytest.fixture
def fen():
    return "rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w - - 0 1"


@pytest.fixture
def legal_moves():
    return ["e1e2"]


def test_legal_moves(mocker, fen, legal_moves):
    mock_get_legal_moves = mocker.patch(
        "xiangqi.lib.pyffish.legal_moves", mocker.MagicMock(return_value=legal_moves)
    )
    assert LegalMoves(fen=fen).result() == legal_moves
    mock_get_legal_moves.assert_called_once_with(fen, [])
