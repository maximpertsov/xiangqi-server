from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie

from xiangqi.models.color import Color
from xiangqi.views.game_mixin import GameMixin


@method_decorator(ensure_csrf_cookie, name="dispatch")
class GameView(GameMixin, View):
    def get(self, request, slug):
        result = {"players": self._players}
        return JsonResponse(result, status=200)

    @property
    def _players(self):
        return [
            {"name": self.game.red_player.username, "color": Color.RED.value},
            {"name": self.game.black_player.username, "color": Color.BLACK.value},
        ]
