import json
from functools import partial

import jsonschema
from django.core import serializers
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.utils.functional import cached_property
from django.views import View

from xiangqi import models
from xiangqi.views import GameMixin

serialize = partial(serializers.serialize, 'json', use_natural_foreign_keys=True)
deserialize = partial(serializers.deserialize, 'json', use_natural_foreign_keys=True)


class GameMoveView(GameMixin, View):
    @property
    def post_schema(self):
        return {
            "properties": {
                "player": {"type": "string"},
                "from": {
                    "type": "array",
                    "items": {"type": "number"},
                    "minItems": 2,
                    "maxItems": 2,
                },
                "to": {
                    "type": "array",
                    "items": {"type": "number"},
                    "minItems": 2,
                    "maxItems": 2,
                },
                "type": {"type": "string"},
            },
            "required": ["player", "from", "to", "type"],
            # TODO: revert to False
            "additionalProperties": True,
        }

    def position(self, rank, file):
        result, _ = models.Position.objects.get_or_create(rank=rank, file=file)
        return result

    def get(self, request, slug):
        serialized = serialize(self.moves.all())
        moves = []
        for data in json.loads(serialized):
            fields = data.pop('fields')
            participant_key = tuple(fields['participant'])
            player = dict(self.players_data_by_participant[participant_key])
            del player['score']

            moves.append(
                {
                    'player': player,
                    'origin': fields['origin'],
                    'destination': fields['destination'],
                }
            )

        return JsonResponse({'moves': moves}, status=200)

    def validate_data(self, payload, slug):
        username = payload.pop('player')
        payload.update(participant=[slug, username])
        payload['origin'] = payload.pop('from')
        payload['destination'] = payload.pop('to')
        # TODO: remove
        payload.pop('piece', None)

        try:
            participant = self.participants.get(player__user__username=username)
        except models.Participant.DoesNotExist:
            raise ValidationError('Invalid player')

        if self.active_participant != participant:
            raise ValidationError('Moving out of turn')

        payload['type'] = models.MoveType.objects.get_or_create(
            name=payload.pop('type')
        )[0].pk
        payload['order'] = self.moves.count() + 1
        payload['notation'] = 'rank,file->rank,file'
        payload['game'] = [slug]

    @cached_property
    def cache_key(self):
        from xiangqi.views import MoveCountView

        game_slug = self.kwargs[self.slug_url_kwarg]
        return MoveCountView.get_cache_key(game_slug)

    def post(self, request, slug):
        try:
            payload = json.loads(request.body.decode("utf-8"))
            jsonschema.validate(payload, self.post_schema)
            self.validate_data(payload, slug)
        except json.JSONDecodeError:
            return JsonResponse({"error": 'Error parsing request'}, status=400)
        except (jsonschema.ValidationError, ValidationError) as e:
            return JsonResponse({"error": str(e)}, status=400)

        data = {'model': 'xiangqi.move', 'fields': payload}

        try:
            deserialized = deserialize(json.dumps([data]))
            for obj in deserialized:
                obj.object.save()
                cache.set(self.cache_key, models.Move.objects.count(), timeout=None)
                return JsonResponse({}, status=201)
        except serializers.base.DeserializationError:
            return JsonResponse({"error": "Could not save move"}, status=400)
