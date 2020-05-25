import pytest

from xiangqi.queries.legal_moves import LegalMoves


@pytest.fixture
def fen():
    return "FEN 0"


@pytest.fixture
def new_fen():
    return "FEN 1"


@pytest.fixture
def legal_move():
    return "e1e2"


def test_legal_moves(mocker, fen, new_fen, legal_move):
    get_legal_moves = mocker.patch(
        "lib.pyffish.xiangqi.legal_moves",
        mocker.MagicMock(return_value=[legal_move]),
    )
    get_fen = mocker.patch(
        "lib.pyffish.xiangqi.get_fen", mocker.MagicMock(return_value=new_fen)
    )
    assert LegalMoves(fen=fen).result == {legal_move: new_fen}
    get_fen.assert_called_once_with(fen, [legal_move])
    get_legal_moves.assert_called_once_with(fen, [])
