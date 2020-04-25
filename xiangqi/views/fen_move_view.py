from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views import View

from xiangqi.queries.serialize_fen import SerializeFen, SerializeInitialFen
from xiangqi.views.payload_schema_mixin import PayloadSchemaMixin


class FenMoveView(PayloadSchemaMixin, View):
    # TODO: make this a separate endpoint
    def get(self, request):
        return JsonResponse(SerializeInitialFen().result(), status=200)

    def post(self, request):
        try:
            return JsonResponse(self._fen_data, status=200)
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)

    @property
    def _fen_data(self):
        fen = self.payload["fen"]
        return SerializeFen(fen=fen).result()

    @property
    def payload_schema(self):
        return {"properties": {"fen": {"type": "string"}}, "required": ["fen"]}
