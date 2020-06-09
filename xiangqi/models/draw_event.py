from enum import Enum

from xiangqi.models.game_event import GameEvent, GameEventManager


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


class DrawEvent(GameEvent):
    objects = DrawEventManager()

    class Meta:
        proxy = True
