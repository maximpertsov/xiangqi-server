import json

import pytest

from xiangqi.queries.serialize_move import SerializeInitialPlacement, SerializeMove


@pytest.fixture
def url():
    return "/api/fen"


@pytest.fixture
def payload():
    return {"fen": "FEN0", "move": "a1a2"}


@pytest.fixture
def serialize_result():
    return {"fen": "FEN1", "move": "a1a2"}


@pytest.fixture
def mock_serialize_move(mocker, serialize_result):
    return mocker.patch.object(SerializeMove, "result", return_value=serialize_result)


def test_post_fen_move_ok(client, url, payload, mock_serialize_move, serialize_result):
    response = client.post(
        url, data=json.dumps(payload), content_type="application/json"
    )
    mock_serialize_move.assert_called_once()
    assert response.status_code == 200
    assert response.json() == {"move": serialize_result}


@pytest.fixture
def mock_serialize_initial_placement(mocker):
    return mocker.patch.object(SerializeInitialPlacement, "result", return_value={})


def test_get_fen_move_ok(client, url, mock_serialize_initial_placement):
    response = client.get(url)
    mock_serialize_initial_placement.assert_called_once()
    assert response.status_code == 200
