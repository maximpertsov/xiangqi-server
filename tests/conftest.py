import json

import pytest
from pytest_factoryboy import LazyFixture, register
from rest_framework.test import APIClient

from tests.factories.game import GameFactory
from tests.factories.game_event import GameEventFactory
from tests.factories.game_request import GameRequestFactory
from tests.factories.move import MoveFactory
from tests.factories.player import PlayerFactory

register(GameEventFactory)
register(GameRequestFactory)
register(MoveFactory)
register(PlayerFactory)
register(PlayerFactory, "player1", username="rosie")
register(PlayerFactory, "player2", username="bob")
register(
    GameFactory,
    slug="ABC123",
    player1=LazyFixture("player1"),
    player2=LazyFixture("player2"),
)

# Utilities


@pytest.fixture
def api_client(player):
    return APIClient()


@pytest.fixture
def call_api(api_client):
    def wrapped(http_method, url, user=None, payload=None):
        if user:
            api_client.force_authenticate(user)

        args = [url]
        kwargs = (
            {"data": json.dumps(payload), "content_type": "application/json"}
            if payload
            else {}
        )

        return getattr(api_client, http_method)(*args, **kwargs)

    return wrapped
