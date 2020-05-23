import pytest
from rest_framework.test import force_authenticate

from xiangqi.views import PositionView, StartingPositionView


@pytest.fixture
def mock_pyffish(mocker):
    return mocker.patch.multiple(
        "lib.pyffish.xiangqi",
        get_fen=mocker.MagicMock(return_value="FEN"),
        gives_check=mocker.MagicMock(return_value=False),
        legal_moves=mocker.MagicMock(return_value=[]),
        start_fen=mocker.MagicMock(return_value="START_FEN"),
    )


@pytest.fixture
def post(rf, player):
    def wrapped(url, data=None):
        request = rf.post(url, data=data, content_type="application/json")
        force_authenticate(request, user=player)
        if url == "/api/position":
            return PositionView.as_view()(request)
        if url == "/api/starting-position":
            return StartingPositionView.as_view()(request)

    return wrapped


@pytest.mark.django_db
def test_position_view(post, mock_pyffish):
    response = post("/api/position", data={"fen": "FEN"})
    assert response.status_code == 200
    assert response.data == {"fen": "FEN", "legal_moves": {}, "gives_check": False}


@pytest.mark.django_db
def test_starting_position_view(post, mock_pyffish):
    response = post("/api/starting-position")
    assert response.status_code == 200
    assert response.data == {
        "fen": "START_FEN",
        "legal_moves": {},
        "gives_check": False,
    }
