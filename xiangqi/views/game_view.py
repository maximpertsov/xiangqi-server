from django.core.cache import cache
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.utils.functional import cached_property
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie

from xiangqi.views import GameMixin


@method_decorator(ensure_csrf_cookie, name="dispatch")
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
        result = {
            'initial_fen': self.initial_fen,
            'players': list(self.players_data_by_participant.values()),
            'title': self.title,
        }
        return JsonResponse(result, status=200)
