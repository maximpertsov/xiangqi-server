import pytest

from xiangqi.queries.legal_moves import LegalMoves
from xiangqi.queries.serialize_move import SerializeMove


@pytest.fixture
def fen():
    return "FEN 0"


@pytest.fixture
def new_fen():
    return "FEN 1"


@pytest.fixture
def new_legal_moves():
    return []


@pytest.mark.django_db
def test_serialize_move(mocker, move__fan, fen, new_fen, new_legal_moves):
    mock_get_fen = mocker.patch(
        "xiangqi.lib.pyffish.xiangqi.get_fen", mocker.MagicMock(return_value=new_fen)
    )
    mock_gives_check = mocker.patch(
        "xiangqi.lib.pyffish.xiangqi.gives_check", mocker.MagicMock(return_value=True)
    )
    mock_query_legal_moves = mocker.patch.object(
        LegalMoves, "result", return_value=new_legal_moves
    )

    assert SerializeMove(fen=fen, fan=move__fan).result() == {
        "fen": new_fen,
        "gives_check": True,
        "legal_moves": new_legal_moves,
        "fan": move__fan,
    }
    mock_get_fen.assert_called_once_with(fen, [move__fan])
    mock_gives_check.assert_called_once_with(new_fen, [])
    mock_query_legal_moves.assert_called_once_with()
