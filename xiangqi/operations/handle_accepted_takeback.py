from django.db import models

from xiangqi.models import Move
from xiangqi.models.takeback_event import TakebackEventTypes


class HandleAcceptedTakeback:
    def perform(self, event):
        self._event = event

        self._takeback_moves()

    # TODO: do this with one query instead of two?
    def _takeback_moves(self):
        if self._rejected_or_canceled:
            return

        Move.objects.filter(game=self._game).filter(
            pk__gte=models.Subquery(
                self._events_since_last_offer.filter(
                    name=TakebackEventTypes.OFFERED_TAKEBACK.value
                ).values("move_set__pk")[0:]
            )
        ).delete()

    @property
    def _rejected_or_canceled(self):
        return self._events_since_last_offer.filter(
            name__in=[
                TakebackEventTypes.CANCELED_TAKEBACK.value,
                TakebackEventTypes.REJECTED_TAKEBACK.value,
            ]
        ).exists()

    @property
    def _game(self):
        return self._event.game

    @property
    def _events_since_last_offer(self):
        return self._game.event_set.filter(
            name__in=TakebackEventTypes.values(),
            created_at__gte=models.Subquery(
                self._game.event_set.filter(
                    game=models.OuterRef("game"),
                    name=TakebackEventTypes.OFFERED_TAKEBACK.value,
                )
                .order_by("-created_at")
                .values("created_at")[0:]
            ),
        )
