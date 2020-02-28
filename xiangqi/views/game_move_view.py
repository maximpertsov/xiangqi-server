import json

import jsonschema
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views import View
from django.views.generic.detail import SingleObjectMixin

from xiangqi.models import Game
from xiangqi.operations.move.persist_move import PersistMove
from xiangqi.queries.move.game_moves import GameMoves


class GameMoveView(SingleObjectMixin, View):
    model = Game

    def get(self, request, slug):
        return JsonResponse({"moves": self._game_moves}, status=200)

    def post(self, request, slug):
        try:
            payload = json.loads(request.body.decode("utf-8"))
            jsonschema.validate(payload, self.post_schema)
            PersistMove(game=self._game, payload=payload).perform()
            return JsonResponse({"moves": self._game_moves}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error parsing request"}, status=400)
        except (jsonschema.ValidationError, ValidationError) as e:
            return JsonResponse({"error": str(e)}, status=400)

    @property
    def post_schema(self):
        return {
            "properties": {"player": {"type": "string"}, "move": {"type": "string"}},
            "required": ["player", "move"],
        }

    @property
    def _game_moves(self):
        return GameMoves(game=self._game).result()

    @property
    def _game(self):
        return self.get_object()
