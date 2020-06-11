from types import SimpleNamespace

import pytest

from xiangqi.queries.legal_moves import LegalMoves
from xiangqi.views import PositionView, StartingPositionView


@pytest.fixture
def mocks(mocker):
    return SimpleNamespace(
        LegalMoves=mocker.patch.object(LegalMoves, "result", return_value={}),
        xiangqi=mocker.patch.multiple(
            "lib.pyffish.xiangqi",
            get_fen=mocker.MagicMock(return_value="FEN"),
            gives_check=mocker.MagicMock(return_value=False),
            start_fen=mocker.MagicMock(return_value="START_FEN"),
        ),
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
    assert mocks.LegalMoves.called_once_with(fen="FEN")
    assert response.status_code == 200
    assert response.data == {"fen": "FEN", "legal_moves": {}, "gives_check": False}


@pytest.mark.django_db
def test_starting_position_view(post, mocks):
    response = post("/api/starting-position")
    assert mocks.LegalMoves.called_once_with(fen="START_FEN")
    assert response.status_code == 200
    assert response.data == {
        "fen": "START_FEN",
        "legal_moves": {},
        "gives_check": False,
    }
