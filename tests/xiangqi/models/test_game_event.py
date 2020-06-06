import pytest
from xiangqi.models import GameEvent


@pytest.fixture
def draw_events(game, game_event_factory):
    return [
        game_event_factory(game=game, name="offered_draw"),
        game_event_factory(game=game, name="rejected_draw"),
        game_event_factory(game=game, name="offered_draw"),
    ]


@pytest.mark.django_db
def test_open_draw_offers(game, draw_events):
    return set(GameEvent.open_draw_offers.all()) == set([draw_events[-1]])
