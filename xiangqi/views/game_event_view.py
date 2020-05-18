from rest_framework.generics import CreateAPIView

from xiangqi.serializers.game_event_serializer import GameEventSerializer


class GameEventView(CreateAPIView):

    # TODO: add authenication to tests
    permission_classes = []
    authentication_classes = []

    serializer_class = GameEventSerializer
