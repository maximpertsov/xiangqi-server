from django.core.cache import cache
from django.http import JsonResponse
from django.utils.functional import cached_property
from django.views.generic.detail import View

from xiangqi.views import GameMixin


class LastUpdateView(GameMixin, View):
    @classmethod
    def get_cache_key(cls, game_slug):
        return 'updated_at_{}'.format(game_slug)

    @cached_property
    def cache_key(self):
        return self.get_cache_key(self.kwargs[self.slug_url_kwarg])

    @cached_property
    def updated_at(self):
        return cache.get(self.cache_key)

    def get(self, request, slug):
        return JsonResponse({'updated_at': self.updated_at}, status=200)
