from pytest_factoryboy import register

from tests.factories.game import GameFactory
from tests.factories.game_event import GameEventFactory
from tests.factories.move import MoveFactory
from tests.factories.participant import ParticipantFactory
from tests.factories.player import PlayerFactory
from tests.factories.user import UserFactory

register(GameFactory)
register(GameEventFactory)
register(PlayerFactory)
register(UserFactory)
register(ParticipantFactory)
register(MoveFactory)
