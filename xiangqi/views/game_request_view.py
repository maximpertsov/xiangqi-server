from rest_framework.generics import CreateAPIView, UpdateAPIView

from xiangqi.serializers.game_request_serializer import GameRequestSerializer


class GameRequestView(CreateAPIView):
    serializer_class = GameRequestSerializer


class JoinGameRequestView(UpdateAPIView):
    serializer_class = GameRequestSerializer
