from django.core.cache import cache
from django.http import JsonResponse
from django.utils.functional import cached_property
from django.views.generic.detail import View

from xiangqi.views.game_mixin import GameMixin
from xiangqi.models.move import Move


class MoveCountView(GameMixin, View):
    @classmethod
    def get_cache_key(cls, game_slug):
        return "updated_at_{}".format(game_slug)

    def get(self, request, slug):
        return JsonResponse({"move_count": self.move_count}, status=200)

    @cached_property
    def move_count(self):
        result = cache.get(self.cache_key)
        if result is None:
            result = Move.objects.count()
            cache.set(self.cache_key, result, timeout=None)

        return result

    @cached_property
    def cache_key(self):
        game_slug = self.kwargs[self.slug_url_kwarg]
        return self.get_cache_key(game_slug)
