from django.core.exceptions import ValidationError
from django.utils.functional import cached_property

from xiangqi.models import GameEvent
from xiangqi.operations.create_move import CreateMove


class CreateGameEvent:
    _EVENT_HANDLER_CLASSES = {"move": CreateMove}

    def __init__(self, game, payload):
        self._game = game
        self._payload = payload

    def perform(self):
        self._handle_event()

    def _handle_event(self):
        try:
            handler = self._EVENT_HANDLER_CLASSES[self._event_name]
            handler(event=self._event).perform()
        except KeyError as event_name:
            # TODO: make event model as failed?
            raise ValidationError("Unknown event {}".format(event_name))

    @cached_property
    def _event(self):
        return GameEvent.objects.create(
            game=self._game, name=self._event_name, payload=self._payload
        )

    @property
    def _event_name(self):
        return self._payload["name"]
