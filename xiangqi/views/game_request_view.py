from rest_framework.generics import CreateAPIView

from xiangqi.serializers.game_request_serializer import GameRequestSerializer


class GameRequestView(CreateAPIView):
    serializer_class = GameRequestSerializer
