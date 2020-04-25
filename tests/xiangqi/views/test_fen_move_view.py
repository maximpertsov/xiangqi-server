import json

import pytest

from xiangqi.queries.serialize_fen import SerializeInitialFen, SerializeFen


@pytest.fixture
def url():
    return "/api/fen"


@pytest.fixture
def payload():
    return {"fen": "FEN"}


@pytest.fixture
def serialize_result():
    return {"fen": "FEN", "legal_moves": {}, "gives_check": False}


@pytest.fixture
def mock_serialize_fen(mocker, serialize_result):
    return mocker.patch.object(SerializeFen, "result", return_value=serialize_result)


def test_post_fen_move_ok(client, url, payload, mock_serialize_fen, serialize_result):
    response = client.post(
        url, data=json.dumps(payload), content_type="application/json"
    )
    mock_serialize_fen.assert_called_once()
    assert response.status_code == 200
    assert response.json() == serialize_result


@pytest.fixture
def mock_serialize_initial_fen(mocker):
    return mocker.patch.object(SerializeInitialFen, "result", return_value={})


def test_get_fen_move_ok(client, url, mock_serialize_initial_fen):
    response = client.get(url)
    mock_serialize_initial_fen.assert_called_once()
    assert response.status_code == 200
