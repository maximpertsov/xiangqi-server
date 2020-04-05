from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie

from xiangqi.queries.game_moves import GameMoves
from xiangqi.queries.game_players import GamePlayers
from xiangqi.views.game_mixin import GameMixin


@method_decorator(ensure_csrf_cookie, name="dispatch")
class GameView(GameMixin, View):
    def get(self, request, slug):
        result = {"players": self._players, "moves": self._game_moves}
        return JsonResponse(result, status=200)

    @property
    def _players(self):
        return GamePlayers(game=self.game).result()

    @property
    def _game_moves(self):
        return GameMoves(game=self.game).result()
