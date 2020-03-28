import json
from functools import partial

from django.core import serializers
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.utils.functional import cached_property

from xiangqi.queries.move.game_moves import GameMoves

deserialize = partial(serializers.deserialize, "json", use_natural_foreign_keys=True)

CACHE_TTL = 3600


class PersistMove:
    def __init__(self, event):
        self._event = event

    def perform(self):
        self._persist_move()

    def _persist_move(self):
        data = {"model": "xiangqi.move", "fields": self._update_attributes}

        try:
            deserialized = deserialize(json.dumps([data]))
            for obj in deserialized:
                obj.object.save()
                cache.set(self._cache_key, self._move_count, timeout=CACHE_TTL)
        except serializers.base.DeserializationError:
            raise ValidationError("Could not save move")

    @cached_property
    def _game_moves(self):
        return GameMoves(game=self._game).result()

    @cached_property
    def _update_attributes(self):
        return {
            "participant": [self._slug, self._username],
            "game": [self._slug],
            "name": self._move_name,
            # "event": self._event,  # TODO: not json serializable
        }

    @cached_property
    def _move_name(self):
        return self._payload["move"]

    @cached_property
    def _cache_key(self):
        from xiangqi.views import MoveCountView

        return MoveCountView.get_cache_key(self._slug)

    @property
    def _move_count(self):
        return self._game.move_set.count()

    @cached_property
    def _slug(self):
        return self._game.slug

    @cached_property
    def _username(self):
        return self._payload["player"]

    @cached_property
    def _game(self):
        return self._event.game

    @cached_property
    def _payload(self):
        return self._event.payload
