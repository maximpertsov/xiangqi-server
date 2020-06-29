from rest_framework.generics import CreateAPIView

from xiangqi.serializers.game_request_serializer import (GameRequestPlayerSerializer,
                                                         GameRequestSerializer)


class GameRequestView(CreateAPIView):
    serializer_class = GameRequestSerializer


class GameRequestPlayerView(CreateAPIView):
    serializer_class = GameRequestPlayerSerializer
