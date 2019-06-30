import json
from functools import partial

from django.core import serializers
from django.http import JsonResponse
from django.views.generic.detail import View

from xiangqi.views import GameMixin

serialize = partial(serializers.serialize, 'json', use_natural_foreign_keys=True)


class GameCurrentPlayerView(GameMixin, View):
    # TODO: cache result for faster polling
    def get(self, request, slug):
        serialized = serialize([self.active_participant])
        data = json.loads(serialized)
        current_player = data[0].pop('fields')['player']
        return JsonResponse({'player': current_player}, status=200)
