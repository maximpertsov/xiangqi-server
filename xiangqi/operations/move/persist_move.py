import json
from functools import partial

from django.core import serializers
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.utils.functional import cached_property

# from xiangqi.queries.move.serialize_move import SerializeMove
# from xiangqi.queries.move.game_moves import GameMoves

serialize = partial(serializers.serialize, 'json', use_natural_foreign_keys=True)
deserialize = partial(serializers.deserialize, 'json', use_natural_foreign_keys=True)


class PersistMove:
    def __init__(self, game, payload):
        self._game = game
        self._payload = payload

    def perform(self):
        self._persist_move()

    def _persist_move(self):
        data = {'model': 'xiangqi.move', 'fields': self._update_attributes}

        try:
            deserialized = deserialize(json.dumps([data]))
            for obj in deserialized:
                # fen = self._fen
                obj.object.save()
                cache.set(self._cache_key, self._move_count + 1, timeout=None)
                # return SerializeMove(fen=fen, move=obj.object)
        except serializers.base.DeserializationError:
            raise ValidationError("Could not save move")

    # @cached_property
    # def _fen(self):
    #     return GameMoves(game=self._game).result()[-1]['fen']

    @cached_property
    def _update_attributes(self):
        return {
            'participant': [self._slug, self._username],
            'order': self._move_count + 1,
            'game': [self._slug],
            'name': self._move_name,
        }

    # TODO: temporary
    @cached_property
    def _move_name(self):
        return self._payload['move']

    # TODO: temporary
    @staticmethod
    def rank_file_to_square(rank, file):
        return '{file}{rank}'.format(rank=10 - rank, file='abcdefghi'[file])

    @cached_property
    def _cache_key(self):
        from xiangqi.views import MoveCountView

        return MoveCountView.get_cache_key(self._slug)

    @cached_property
    def _move_count(self):
        return self._game.move_set.count()

    @cached_property
    def _slug(self):
        return self._game.slug

    @cached_property
    def _username(self):
        return self._payload['player']
