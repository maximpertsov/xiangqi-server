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
    assert set(GameEvent.open_draw_offers.all()) == set([draw_events[-1]])


@pytest.fixture
def draw_events_multiple_games(game_factory, game_event_factory):
    game1, game2 = game_factory.create_batch(2)
    return {
        game1: [
            game_event_factory(game=game1, name="offered_draw"),
            game_event_factory(game=game1, name="rejected_draw"),
            game_event_factory(game=game1, name="offered_draw"),
        ],
        game2: [
            game_event_factory(game=game2, name="offered_draw"),
            game_event_factory(game=game2, name="rejected_draw"),
            game_event_factory(game=game2, name="offered_draw"),
        ],
    }


@pytest.mark.django_db
def test_open_draw_offers_multiple_games(draw_events_multiple_games):
    for game, events in draw_events_multiple_games.items():
        assert set(GameEvent.open_draw_offers.filter(game=game)) == set([events[-1]])
