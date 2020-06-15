from enum import Enum

from xiangqi.models.game_event import GameEvent, GameEventManager, UnresolvedEventQuerySet


class DrawEventTypes(Enum):
    ACCEPTED_DRAW = "accepted_draw"
    CANCELED_DRAW = "canceled_draw"
    OFFERED_DRAW = "offered_draw"
    REJECTED_DRAW = "rejected_draw"

    @classmethod
    def values(cls):
        return [tag.value for tag in cls]


class DrawEventManager(GameEventManager):
    def get_queryset(self):
        return super().get_queryset().filter(name__in=DrawEventTypes.values())


class OpenDrawOffersManager(DrawEventManager):
    def get_queryset(self):
        return UnresolvedEventQuerySet(
            self.model,
            using=self._db,
            open_events=[DrawEventTypes.OFFERED_DRAW.value],
            close_events=[
                DrawEventTypes.ACCEPTED_DRAW.value,
                DrawEventTypes.CANCELED_DRAW.value,
                DrawEventTypes.REJECTED_DRAW.value,
            ],
        )


class DrawEvent(GameEvent):
    objects = DrawEventManager()
    open_offers = OpenDrawOffersManager()

    class Meta:
        proxy = True
