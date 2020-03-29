from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie

from xiangqi.views.game_mixin import GameMixin


@method_decorator(ensure_csrf_cookie, name="dispatch")
class GameView(GameMixin, View):
    def get(self, request, slug):
        result = {"players": list(self._players)}
        return JsonResponse(result, status=200)

    @property
    def _players(self):
        for participant in self.game.participant_set.all():
            yield {
                "name": participant.player.user.username,
                "color": participant.color,
                "score": participant.score,
            }
