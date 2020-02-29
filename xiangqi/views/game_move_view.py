from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views import View
from django.views.generic.detail import SingleObjectMixin

from xiangqi.models import Game
from xiangqi.operations.move.persist_move import PersistMove
from xiangqi.queries.move.game_moves import GameMoves
from xiangqi.views.payload_schema_mixin import PayloadSchemaMixin


class GameMoveView(SingleObjectMixin, PayloadSchemaMixin, View):
    model = Game

    def get(self, request, slug):
        return JsonResponse({"moves": self._game_moves}, status=200)

    def post(self, request, slug):
        try:
            self._persist_move()
            return JsonResponse({"move": self._latest_game_move}, status=201)
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)

    def _persist_move(self):
        PersistMove(game=self._game, payload=self.payload).perform()

    @property
    def _latest_game_move(self):
        return self._game_moves[-1]

    @property
    def _game_moves(self):
        return GameMoves(game=self._game).result()

    @property
    def _game(self):
        return self.get_object()

    @property
    def payload_schema(self):
        return {
            "properties": {"player": {"type": "string"}, "move": {"type": "string"}},
            "required": ["player", "move"],
        }
