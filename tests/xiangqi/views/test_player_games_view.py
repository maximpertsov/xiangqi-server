import json
from types import SimpleNamespace

import pytest
from rest_framework.test import APIClient

from xiangqi.models.team import Team
from xiangqi.queries.legal_moves import LegalMoves


@pytest.fixture
def mocks(mocker):
    return SimpleNamespace(
        LegalMoves=mocker.patch.object(LegalMoves, "result", return_value={}),
        xiangqi=mocker.patch.multiple(
            "lib.pyffish.xiangqi",
            gives_check=mocker.MagicMock(return_value=False),
            start_fen=mocker.MagicMock(return_value="START_FEN"),
        ),
    )


@pytest.fixture
def api_client(player):
    return APIClient()


@pytest.fixture
def call_api(api_client):
    def wrapped(http_method, url, user=None, payload=None):
        api_client.force_authenticate(user)

        args = [url]
        kwargs = (
            {"data": json.dumps(payload), "content_type": "application/json"}
            if payload
            else {}
        )

        return getattr(api_client, http_method)(*args, **kwargs)

    return wrapped


@pytest.mark.django_db
def test_get_games_for_player(call_api, game, mocks):
    url = "/api/player/{}/games".format(game.player1.username)
    response = call_api("get", url, user=game.player1)
    assert response.status_code == 200

    print(response.json())

    assert response.json() == {
        "games": [
            {
                "slug": game.slug,
                "current_move": {
                    "fen": "START_FEN",
                    "gives_check": False,
                    "legal_moves": {},
                },
                "score1": 0.0,
                "score2": 0.0,
                "player1": {"team": Team.RED.value, "name": "rosie"},
                "player2": {"team": Team.BLACK.value, "name": "bob"},
                "open_takeback_offer": None,
                "open_draw_offer": None,
            }
        ]
    }


@pytest.mark.django_db
def test_get_games_for_player_without_active_games(call_api, game):
    game.finish(0.5, 0.5)
    url = "/api/player/{}/games".format(game.player1.username)
    response = call_api("get", url, user=game.player1)
    assert response.status_code == 200
    assert response.json() == {"games": []}
