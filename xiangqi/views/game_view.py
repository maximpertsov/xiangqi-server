from rest_framework.generics import CreateAPIView, RetrieveAPIView

from xiangqi.models import Game
from xiangqi.serializers.game_serializer import GameSerializer


class GameView(RetrieveAPIView):
    serializer_class = GameSerializer
    queryset = Game.objects.all()
    lookup_field = "slug"


class CreateGameView(CreateAPIView):
    serializer_class = GameSerializer
