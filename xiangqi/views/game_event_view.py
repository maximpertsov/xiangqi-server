from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views import View
from rest_framework.generics import CreateAPIView

from xiangqi.operations.create_game_event import CreateGameEvent
from xiangqi.serializers.game_event_serializer import GameEventSerializer
from xiangqi.views.game_mixin import GameMixin
from xiangqi.views.payload_schema_mixin import PayloadSchemaMixin


class GameEventView(GameMixin, PayloadSchemaMixin, View):
    def post(self, request, slug):
        try:
            self._create_event()
            return JsonResponse({}, status=201)
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)

    def _create_event(self):
        CreateGameEvent(game=self.game, payload=self.payload).perform()

    @property
    def payload_schema(self):
        return {"name": "string"}


class GameEventCreateView(CreateAPIView):

    # TODO: add authenication to tests
    permission_classes = []
    authentication_classes = []

    serializer_class = GameEventSerializer
