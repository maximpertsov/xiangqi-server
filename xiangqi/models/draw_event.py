from enum import Enum

from django.db import models
from django.utils.timezone import datetime

from xiangqi.models.game_event import GameEvent


class DrawEventTypes(Enum):
    ACCEPTED_DRAW = "accepted_draw"
    CANCELED_DRAW = "canceled_draw"
    OFFERED_DRAW = "offered_draw"
    REJECTED_DRAW = "rejected_draw"

    @classmethod
    def values(cls):
        return [tag.value for tag in cls]


class DrawEventManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(name__in=DrawEventTypes.values())


class OpenDrawOffersManager(DrawEventManager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                name=DrawEventTypes.OFFERED_DRAW.value,
                created_at__gt=models.Subquery(
                    self._last_responses_to_draw_offer_datetime()
                ),
            )
        )

    def _last_responses_to_draw_offer_datetime(self):
        return (
            super()
            .get_queryset()
            .filter(game=models.OuterRef("game"), name__in=DrawEventTypes.values())
            .annotate(
                _created_at=models.Case(
                    models.When(
                        name=DrawEventTypes.OFFERED_DRAW.value, then=datetime.min
                    ),
                    default=models.F("created_at"),
                )
            )
            .values("game")
            .annotate(result=models.Max("_created_at"))
            .values("result")[:1]
        )


class DrawEvent(GameEvent):
    objects = DrawEventManager()
    open_offers = OpenDrawOffersManager()

    class Meta:
        proxy = True
