from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views import View

from xiangqi.queries.move.serialize_move import SerializeInitialPlacement, SerializeMove
from xiangqi.views.payload_schema_mixin import PayloadSchemaMixin


class FenMoveView(PayloadSchemaMixin, View):
    # TODO: make this a separate endpoint
    def get(self, request):
        return JsonResponse({"move": SerializeInitialPlacement().result()}, status=200)

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

    @property
    def payload_schema(self):
        return {
            "properties": {"fen": {"type": "string"}, "move": {"type": "string"}},
            "required": ["fen", "move"],
        }
