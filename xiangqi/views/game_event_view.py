from rest_framework.generics import CreateAPIView

from xiangqi.serializers.game_event_serializer import GameEventSerializer


class GameEventView(CreateAPIView):
    serializer_class = GameEventSerializer
