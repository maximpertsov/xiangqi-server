from rest_framework.generics import RetrieveAPIView

from xiangqi.models import Game
from xiangqi.serializers.game_serializer import GameSerializer


class GameView(RetrieveAPIView):
    # TODO: remove
    authentication_classes = []
    permission_classes = []

    serializer_class = GameSerializer
    queryset = Game.objects.all()
    lookup_field = "slug"
