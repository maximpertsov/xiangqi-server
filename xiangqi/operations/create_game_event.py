from django.core.exceptions import ValidationError
from django.db.transaction import atomic
from django.utils.functional import cached_property

from xiangqi.models import Game, GameEvent
from xiangqi.operations.create_move import CreateMove


class CreateGameEvent:
    _EVENT_HANDLER_CLASSES = {"move": CreateMove}

    def __init__(self, game, payload):
        self._game = game
        self._payload = payload

    def perform(self):
        self._handle_event()

    @atomic
    def _handle_event(self):
        try:
            self._game.shuttle(self._event)
            self._handler(event=self._event).perform()
        except Game.TransitionError:
            raise ValidationError("No update")

    @property
    def _handler(self):
        try:
            return self._EVENT_HANDLER_CLASSES[self._event_name]
        except KeyError as event_name:
            raise ValidationError("Unknown event {}".format(event_name))

    @cached_property
    def _event(self):
        return GameEvent.objects.create(
            game=self._game, name=self._event_name, payload=self._payload
        )

    @property
    def _event_name(self):
        return self._payload["name"]
