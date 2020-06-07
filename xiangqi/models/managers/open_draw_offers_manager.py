from django.db import models
from django.utils.timezone import datetime


class OpenDrawOffersManager(models.Manager):
    class Failed(Exception):
        pass

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                name="offered_draw",
                created_at__gt=models.Subquery(
                    self._last_draw_offer_response_datetime()
                ),
            )
        )

    def _last_draw_offer_response_datetime(self):
        return (
            super()
            .get_queryset()
            .filter(
                game=models.OuterRef("game"),
                name__in=["offered_draw", "accepted_draw", "rejected_draw"],
            )
            .annotate(
                _created_at=models.Case(
                    models.When(name="offered_draw", then=datetime.min),
                    default=models.F("created_at"),
                )
            )
            .values("game")
            .annotate(_created_at__max=models.Max("_created_at"))
            .values("_created_at__max")[:1]
        )
