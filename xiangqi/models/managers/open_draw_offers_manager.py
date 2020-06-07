from django.db import models


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
                name__in=["accepted_draw", "rejected_draw"],
            )
            .values("name")
            .annotate(models.Max("created_at"))
            .values("created_at__max")[:1]
        )
