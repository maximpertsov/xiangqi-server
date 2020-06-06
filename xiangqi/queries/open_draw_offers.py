from django.db import models


class OpenDrawOffersManager(models.Manager):
    def open_draw_offers(self):
        return self.filter(
            name="offered_draw",
            created_at__gt=models.Subquery(self._last_draw_offer_response_datetime),
        )

    def _last_draw_offer_response_datetime(self):
        return (
            self.filter(name__in=["accepted_draw", "rejected_draw"])
            .values("name")
            .annotate(models.Max("created_at"))
            .values("created_at__max")[:1]
        )
