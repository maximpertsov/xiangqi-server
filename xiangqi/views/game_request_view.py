from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin, ListModelMixin,
                                   UpdateModelMixin)
from rest_framework.viewsets import GenericViewSet

from xiangqi.models import GameRequest
from xiangqi.serializers.game_request_serializer import GameRequestSerializer


class GameRequestView(
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    serializer_class = GameRequestSerializer
    queryset = GameRequest.objects.filter(player2__isnull=True)
