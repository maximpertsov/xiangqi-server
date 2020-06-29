from pytest_factoryboy import LazyFixture, register

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
