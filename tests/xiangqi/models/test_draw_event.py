import pytest

from xiangqi.models.draw_event import DrawEvent, DrawEventTypes


@pytest.fixture
def draw_events(game, game_event_factory):
    return [
        game_event_factory(game=game, name=DrawEventTypes.OFFERED_DRAW.value),
        game_event_factory(game=game, name=DrawEventTypes.OFFERED_DRAW.value),
    ]


@pytest.mark.django_db
def test_open_draw_offers(game, draw_events):
    assert set(DrawEvent.open_offers.all()) == set(draw_events)


@pytest.fixture
def draw_events_with_responses(game, game_event_factory):
    return [
        game_event_factory(game=game, name=DrawEventTypes.OFFERED_DRAW.value),
        game_event_factory(game=game, name=DrawEventTypes.ACCEPTED_DRAW.value),
        game_event_factory(game=game, name=DrawEventTypes.OFFERED_DRAW.value),
        game_event_factory(game=game, name=DrawEventTypes.REJECTED_DRAW.value),
        game_event_factory(game=game, name=DrawEventTypes.OFFERED_DRAW.value),
        game_event_factory(game=game, name=DrawEventTypes.CANCELED_DRAW.value),
        game_event_factory(game=game, name=DrawEventTypes.OFFERED_DRAW.value),
    ]


@pytest.mark.django_db
def test_open_draw_offers_with_rejections(game, draw_events_with_responses):
    assert set(DrawEvent.open_offers.all()) == set([draw_events_with_responses[-1]])


@pytest.fixture
def draw_events_multiple_games(game_factory, game_event_factory):
    game1, game2 = game_factory.create_batch(2)
    return {
        game1: [
            game_event_factory(game=game1, name=DrawEventTypes.OFFERED_DRAW.value),
            game_event_factory(game=game1, name=DrawEventTypes.ACCEPTED_DRAW.value),
            game_event_factory(game=game1, name=DrawEventTypes.OFFERED_DRAW.value),
        ],
        game2: [
            game_event_factory(game=game2, name=DrawEventTypes.OFFERED_DRAW.value),
            game_event_factory(game=game2, name=DrawEventTypes.ACCEPTED_DRAW.value),
            game_event_factory(game=game2, name=DrawEventTypes.OFFERED_DRAW.value),
        ],
    }


@pytest.mark.django_db
def test_open_draw_offers_multiple_games(draw_events_multiple_games):
    for game, events in draw_events_multiple_games.items():
        assert set(DrawEvent.open_offers.filter(game=game)) == set([events[-1]])
