from rest_framework.generics import CreateAPIView, UpdateAPIView

from xiangqi.serializers.game_request_serializer import GameRequestSerializer
from xiangqi.models import GameRequest


class CreateGameRequestView(CreateAPIView):
    serializer_class = GameRequestSerializer


class UpdateGameRequestView(UpdateAPIView):
    serializer_class = GameRequestSerializer
    queryset = GameRequest.objects.all()
