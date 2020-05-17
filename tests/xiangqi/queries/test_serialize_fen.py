import pytest

from xiangqi.queries.legal_moves import LegalMoves
from xiangqi.queries.serialize_fen import SerializeFen


@pytest.fixture
def fen():
    return "FEN"


@pytest.fixture
def legal_moves():
    return {}


@pytest.fixture
def mock_gives_check(mocker):
    return mocker.patch(
        "lib.pyffish.xiangqi.gives_check", mocker.MagicMock(return_value=True)
    )


@pytest.fixture
def mock_legal_moves(mocker, legal_moves):
    return mocker.patch.object(LegalMoves, "result", return_value=legal_moves)


@pytest.mark.django_db
def test_serialize_fen(fen, legal_moves, mock_gives_check, mock_legal_moves):
    assert SerializeFen(fen=fen).result() == {
        "fen": fen,
        "gives_check": True,
        "legal_moves": legal_moves,
    }
    mock_gives_check.assert_called_once_with(fen, [])
    mock_legal_moves.assert_called_once_with()
