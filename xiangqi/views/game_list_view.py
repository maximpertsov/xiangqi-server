from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.utils.functional import cached_property
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.detail import SingleObjectMixin, View

from xiangqi.models import Player


@method_decorator(ensure_csrf_cookie, name="dispatch")
class GameListView(SingleObjectMixin, View):
    model = Player
    slug_field = "username"
    slug_url_kwarg = "username"

    def get(self, request, username):
        return JsonResponse({"games": list(self._games_data)}, status=200)

    @property
    def _games_data(self):
        for game in self._games:
            yield {"slug": game.slug}

    @cached_property
    def _games(self):
        return self._player.games

    @property
    def _player(self):
        return self.get_object()
