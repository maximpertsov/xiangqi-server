import json

import jsonschema
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.utils.functional import cached_property
from django.views import View

from xiangqi.queries.move.serialize_move import SerializeMove


class FenMoveView(View):
    def post(self, request):
        try:
            return JsonResponse({"move": self._next_move}, status=200)
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)

    @property
    def _next_move(self):
        fen = self.payload["fen"]
        move_name = self.payload["move"]
        return SerializeMove(fen=fen, move_name=move_name).result()

    @cached_property
    def payload(self):
        try:
            result = json.loads(self.request.body.decode("utf-8"))
            jsonschema.validate(result, self.post_schema)
            return result
        except json.JSONDecodeError:
            return ValidationError("Error parsing request")
        except jsonschema.ValidationError as e:
            return ValidationError(str(e))

    @property
    def post_schema(self):
        return {
            "properties": {"fen": {"type": "string"}, "move": {"type": "string"}},
            "required": ["fen", "move"],
        }
