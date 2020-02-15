import json

import jsonschema
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views import View

from xiangqi.operations.move import CreateMove
from xiangqi.queries.move import GameMoves
from xiangqi.views import GameMixin


class GameMoveView(GameMixin, View):
    def get(self, request, slug):
        return JsonResponse({"moves": GameMoves(game=self.game).result()}, status=200)

    def post(self, request, slug):
        try:
            payload = json.loads(request.body.decode("utf-8"))
            jsonschema.validate(payload, self.post_schema)
            CreateMove(game=self.game, payload=payload).perform()
            return JsonResponse({}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error parsing request"}, status=400)
        except (jsonschema.ValidationError, ValidationError) as e:
            return JsonResponse({"error": str(e)}, status=400)

    @property
    def post_schema(self):
        return {
            "properties": {
                "player": {"type": "string"},
                "move": {"type": "string"},
            },
            "required": ["player", "move"],
        }
