import pytest

from xiangqi.queries.legal_moves import LegalMoves
from xiangqi.queries.position import Position


@pytest.fixture
def mock_pyffish(mocker):
    return mocker.patch.multiple(
        "xiangqi.lib.pyffish.xiangqi",
        get_fen=mocker.DEFAULT,
        gives_check=mocker.DEFAULT,
    )


@pytest.fixture
def mock_legal_moves(mocker):
    return {
        "__init__": mocker.patch.object(LegalMoves, "__init__", return_value=None),
        "result": mocker.patch.object(LegalMoves, "result", return_value={"b10c8": []}),
    }


@pytest.mark.django_db
def test_serialize_fen(mock_pyffish, mock_legal_moves):
    mock_pyffish["get_fen"].return_value = "NEXT_FEN"
    mock_pyffish["gives_check"].return_value = False

    assert Position(previous_fen="START_FEN", move_name="b10c8").result() == {
        "fen": "NEXT_FEN",
        "gives_check": False,
        "legal_moves": {"b10c8": []},
    }

    mock_pyffish["get_fen"].assert_called_once_with("START_FEN", ["b10c8"])
    mock_pyffish["gives_check"].assert_called_once_with("NEXT_FEN", [])
    mock_legal_moves["__init__"].assert_called_once_with(fen="NEXT_FEN")
