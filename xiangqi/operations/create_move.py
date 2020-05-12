import json
from functools import partial

from django.core import serializers
from django.core.exceptions import ValidationError
from django.utils.functional import cached_property

deserialize = partial(serializers.deserialize, "json", use_natural_foreign_keys=True)


class CreateMove:
    def __init__(self, event):
        self._event = event

    def perform(self):
        self._create_move()

    def _create_move(self):
        try:
            for obj in self._deserialized_update:
                if self._previous_move:
                    obj.previous_move = self._previous_move
                obj.object.save()
        except serializers.base.DeserializationError:
            raise ValidationError("Could not save move")

    @property
    def _deserialized_update(self):
        return deserialize(json.dumps(self._update))

    @property
    def _update(self):
        return [{"model": "xiangqi.move", "fields": self._update_attributes}]

    @property
    def _update_attributes(self):
        return {
            "game": [self._slug],
            "name": self._move_name,
            "player": [self._username],
        }

    @cached_property
    def _move_name(self):
        return self._payload["move"]

    @cached_property
    def _slug(self):
        return self._game.slug

    @cached_property
    def _username(self):
        return self._payload["player"]

    @cached_property
    def _previous_move(self):
        return self._game.move_set.order_by('-pk').first()

    @cached_property
    def _game(self):
        return self._event.game

    @cached_property
    def _payload(self):
        return self._event.payload
