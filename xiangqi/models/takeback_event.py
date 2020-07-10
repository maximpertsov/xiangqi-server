from enum import Enum

from django.db import models
from django.utils.timezone import datetime

from xiangqi.models.game_event import GameEvent


class TakebackEventTypes(Enum):
    ACCEPTED_TAKEBACK = "accepted_takeback"
    CANCELED_TAKEBACK = "canceled_takeback"
    OFFERED_TAKEBACK = "offered_takeback"
    REJECTED_TAKEBACK = "rejected_takeback"

    @classmethod
    def values(cls):
        return [tag.value for tag in cls]


class TakebackEventManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(name__in=TakebackEventTypes.values())


class OpenTakebackOffersManager(TakebackEventManager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                name=TakebackEventTypes.OFFERED_TAKEBACK.value,
                created_at__gt=models.Subquery(
                    self._last_responses_to_takeback_offer_datetime()
                ),
            )
        )

    def _last_responses_to_takeback_offer_datetime(self):
        return (
            super()
            .get_queryset()
            .filter(game=models.OuterRef("game"), name__in=TakebackEventTypes.values())
            .annotate(
                _created_at=models.Case(
                    models.When(
                        name=TakebackEventTypes.OFFERED_TAKEBACK.value,
                        then=datetime.min,
                    ),
                    default=models.F("created_at"),
                )
            )
            .values("game")
            .annotate(result=models.Max("_created_at"))
            .values("result")[:1]
        )


class TakebackEvent(GameEvent):
    objects = TakebackEventManager()
    open_offers = OpenTakebackOffersManager()

    class Meta:
        proxy = True
