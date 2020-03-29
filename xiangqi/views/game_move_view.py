from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views import View

from xiangqi.operations.create_move import CreateMove
from xiangqi.queries.move.game_moves import GameMoves
from xiangqi.views.game_mixin import GameMixin
from xiangqi.views.payload_schema_mixin import PayloadSchemaMixin


class GameMoveView(GameMixin, PayloadSchemaMixin, View):
    def get(self, request, slug):
        return JsonResponse({"moves": self._game_moves}, status=200)

    def post(self, request, slug):
        try:
            self._create_move()
            return JsonResponse({"move": self._latest_game_move}, status=201)
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)

    def _create_move(self):
        CreateMove(game=self.game, payload=self.payload).perform()

    @property
    def _latest_game_move(self):
        return self._game_moves[-1]

    @property
    def _game_moves(self):
        return GameMoves(game=self.game).result()

    @property
    def payload_schema(self):
        return {
            "properties": {"player": {"type": "string"}, "move": {"type": "string"}},
            "required": ["player", "move"],
        }
