from django.http import JsonResponse
from django.views import View

from xiangqi.queries.move.game_moves import GameMoves
from xiangqi.views.game_mixin import GameMixin


class GameMoveView(GameMixin, View):
    def get(self, request, slug):
        return JsonResponse({"moves": self._game_moves}, status=200)

    @property
    def _game_moves(self):
        return GameMoves(game=self.game).result()
