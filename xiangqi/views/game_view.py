import json
from functools import partial

from django.core import serializers
from django.core.cache import cache
from django.http import JsonResponse
from django.utils.functional import cached_property
from django.views.generic.detail import View

from xiangqi.views import GameMixin

serialize = partial(serializers.serialize, 'json', use_natural_foreign_keys=True)


class GameView(GameMixin, View):
    @cached_property
    def cache_key(self):
        return 'initial_fen_{}'.format(self.kwargs[self.slug_url_kwarg])

    @cached_property
    def initial_fen(self):
        result = cache.get(self.cache_key)
        if result is None:
            result = self.board_fen(self.initial_board)
            cache.set(self.cache_key, result, 100)
        return result

    def get(self, request, slug):
        serialized = serialize([self.game])
        result = json.loads(serialized)[0]['fields']
        del result['board_dimensions']
        result['ranks'] = self.ranks
        result['files'] = self.files
        result['initial_fen'] = self.initial_fen
        result['players'] = list(self.players_data_by_participant.values())
        # TODO add test
        result['active_color'] = getattr(self.active_participant, 'color', 'red')
        return JsonResponse(result, status=200)
