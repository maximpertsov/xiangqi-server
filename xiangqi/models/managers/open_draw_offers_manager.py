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

    # TODO: group by games
    def _last_draw_offer_response_datetime(self):
        return (
            super()
            .get_queryset()
            .filter(name__in=["accepted_draw", "rejected_draw"])
            .values("name")
            .annotate(models.Max("created_at"))
            .values("created_at__max")
        )

    # TODO use this instead
    def _get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(name__contains="draw")
            .annotate(
                latest_created_at=models.Window(
                    expression=models.Max(
                        "created_at",
                        filter=models.Q(name__in=["accepted_draw", "rejected_draw"]),
                    ),
                    partition_by=[models.F("game")],
                )
            )
        )
