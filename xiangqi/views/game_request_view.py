from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

from xiangqi.models import GameRequest
from xiangqi.serializers.game_request_serializer import GameRequestSerializer


class GameRequestView(
    ListModelMixin, CreateModelMixin, UpdateModelMixin, GenericViewSet
):
    serializer_class = GameRequestSerializer
    queryset = GameRequest.objects.filter(player2__isnull=True)
