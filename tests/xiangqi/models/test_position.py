import pytest

from xiangqi.models.position import Position
from xiangqi.queries.legal_moves import LegalMoves


@pytest.fixture
def mock_pyffish(mocker):
    mocked = mocker.patch.multiple(
        "xiangqi.lib.pyffish.xiangqi",
        get_fen=mocker.DEFAULT,
        gives_check=mocker.DEFAULT,
        start_fen=mocker.DEFAULT,
    )
    mocked["start_fen"].return_value = "START_FEN"
    mocked["get_fen"].return_value = "NEXT_FEN"
    mocked["gives_check"].return_value = False

    return mocked


@pytest.fixture
def mock_legal_moves(mocker):
    mocker.patch.object(LegalMoves, "result", return_value={"b10c8": []}),
    return mocker.patch.object(LegalMoves, "__init__", return_value=None)


@pytest.fixture
def test_common(mock_pyffish, mock_legal_moves):
    def wrapped(**kwargs):
        position = Position(**kwargs)
        assert position.fen == "NEXT_FEN"
        assert position.gives_check is False
        assert position.legal_moves == {"b10c8": []}
        mock_pyffish["gives_check"].assert_called_once_with("NEXT_FEN", [])
        mock_legal_moves.assert_called_once_with(fen="NEXT_FEN")

    return wrapped


@pytest.mark.django_db
def test_position(test_common, mock_pyffish):
    test_common()
    mock_pyffish["get_fen"].assert_called_once_with("START_FEN", [])


@pytest.mark.django_db
def test_position_from_fen(test_common, mock_pyffish):
    test_common(fen="FEN")
    mock_pyffish["get_fen"].assert_called_once_with("FEN", [])


@pytest.mark.django_db
def test_position_with_move(test_common, mock_pyffish):
    test_common(move_name="b10c8")
    mock_pyffish["get_fen"].assert_called_once_with("START_FEN", ["b10c8"])


@pytest.mark.django_db
def test_position_from_fen_with_move(test_common, mock_pyffish):
    test_common(fen="FEN", move_name="b10c8")
    mock_pyffish["get_fen"].assert_called_once_with("FEN", ["b10c8"])
