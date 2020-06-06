from django.db import models


class OpenDrawOffersManager(models.Manager):
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

    # TODO: group by games
    def _last_draw_offer_response_datetime(self):
        return (
            super()
            .get_queryset()
            .filter(name__in=["accepted_draw", "rejected_draw"])
            .values("name")
            .annotate(models.Max("created_at"))
            .values("created_at__max")[:1]
        )
