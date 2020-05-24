import pytest

from xiangqi.queries.game_result import GameResult
from xiangqi.queries.legal_moves import LegalMoves
from xiangqi.views import PositionView, StartingPositionView


@pytest.fixture
def mocks(mocker):
    mocker.patch.object(
        GameResult, "result", new_callable=mocker.PropertyMock, return_value=[0, 0]
    )
    mocker.patch.object(
        LegalMoves, "result", new_callable=mocker.PropertyMock, return_value={}
    )
    mocker.patch.multiple(
        "lib.pyffish.xiangqi",
        get_fen=mocker.MagicMock(return_value="FEN"),
        gives_check=mocker.MagicMock(return_value=False),
        start_fen=mocker.MagicMock(return_value="START_FEN"),
    )


@pytest.fixture
def post(rf, player):
    def wrapped(url, data=None):
        request = rf.post(url, data=data, content_type="application/json")
        if url == "/api/position":
            return PositionView.as_view()(request)
        if url == "/api/starting-position":
            return StartingPositionView.as_view()(request)

    return wrapped


@pytest.mark.django_db
def test_position_view(post, mocks):
    response = post("/api/position", data={"fen": "FEN"})
    assert response.status_code == 200
    assert response.data == {
        "fen": "FEN",
        "legal_moves": {},
        "gives_check": False,
        "game_result": [0, 0],
    }


@pytest.mark.django_db
def test_starting_position_view(post, mocks):
    response = post("/api/starting-position")
    assert response.status_code == 200
    assert response.data == {
        "fen": "START_FEN",
        "legal_moves": {},
        "gives_check": False,
        "game_result": [0, 0],
    }
