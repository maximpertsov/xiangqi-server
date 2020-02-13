import json
from functools import partial

from django.core import serializers
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.utils.functional import cached_property

from xiangqi import models

serialize = partial(serializers.serialize, 'json', use_natural_foreign_keys=True)
deserialize = partial(serializers.deserialize, 'json', use_natural_foreign_keys=True)


class Create:
    def __init__(self, game, payload):
        self.game = game
        self.payload = payload

    def perform(self):
        self.create_move()

    def create_move(self):
        data = {'model': 'xiangqi.move', 'fields': self.update_attributes}

        try:
            deserialized = deserialize(json.dumps([data]))
            for obj in deserialized:
                obj.object.save()
                cache.set(self.cache_key, self.move_count, timeout=None)
        except serializers.base.DeserializationError:
            return ValidationError("Could not save move")

    @cached_property
    def update_attributes(self):
        # TODO: maybe this check can be on the client side for now?
        # if self.active_participant != self.participant:
        #     raise ValidationError('Moving out of turn')

        return {
            'participant': [self.slug, self.username],
            'origin': self.payload['from'],
            'destination': self.payload['to'],
            'order': self.move_count + 1,
            'game': [self.slug],
        }

    @cached_property
    def cache_key(self):
        from xiangqi.views import MoveCountView

        return MoveCountView.get_cache_key(self.slug)

    @cached_property
    def move_count(self):
        return models.Move.objects.count()

    # TODO: maybe this isn't necessary since we are using natural keys?
    # @cached_property
    # def participant(self):
    #     try:
    #         return self.game.participant_set.get(player__user__username=self.username)
    #     except models.Participant.DoesNotExist:
    #         raise ValidationError('Invalid player')

    @cached_property
    def slug(self):
        return self.game.slug

    @cached_property
    def username(self):
        return self.payload.pop('player')
