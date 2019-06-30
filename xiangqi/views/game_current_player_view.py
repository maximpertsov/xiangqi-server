from django.core.cache import cache
from django.http import JsonResponse
from django.utils.functional import cached_property
from django.views.generic.detail import View

from xiangqi.views import GameMixin

CACHE_TTL = 3600


class GameCurrentPlayerView(GameMixin, View):
    @cached_property
    def cache_key(self):
        return 'current_player_{}'.format(self.kwargs[self.slug_url_kwarg])

    @cached_property
    def current_player(self):
        result = cache.get(self.cache_key)
        if result is None:
            result = self.active_participant.player.user.username
            cache.set(self.cache_key, result, CACHE_TTL)
        return result

    # TODO: cache result for faster polling
    def get(self, request, slug):
        return JsonResponse({'player': self.current_player}, status=200)
