from pytest_factoryboy import LazyFixture, register

from tests.factories.game import GameFactory
from tests.factories.game_event import GameEventFactory
from tests.factories.move import MoveFactory
from tests.factories.player import PlayerFactory

register(GameEventFactory)
register(MoveFactory)
register(PlayerFactory)
register(PlayerFactory, "red_player", username="alice")
register(PlayerFactory, "black_player", username="bob")
register(
    GameFactory,
    slug="ABC123",
    red_player=LazyFixture("red_player"),
    black_player=LazyFixture("black_player"),
)
