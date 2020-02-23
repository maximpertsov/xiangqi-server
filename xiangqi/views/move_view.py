import json

import jsonschema
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views import View


class MoveView(View):
    def post(self, request):
        try:
            payload = json.loads(request.body.decode("utf-8"))
            jsonschema.validate(payload, self.post_schema)
            # TODO: calculate next move and return it
            return JsonResponse({}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error parsing request"}, status=400)
        except (jsonschema.ValidationError, ValidationError) as e:
            return JsonResponse({"error": str(e)}, status=400)

    @property
    def post_schema(self):
        return {
            "properties": {"fen": {"type": "string"}, "move": {"type": "string"}},
            "required": ["fen", "move"],
        }
