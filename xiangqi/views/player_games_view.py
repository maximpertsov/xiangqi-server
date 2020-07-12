from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.utils.functional import cached_property
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.detail import SingleObjectMixin, View
from rest_framework import serializers
from rest_framework.generics import RetrieveAPIView

from xiangqi.models import Player
from xiangqi.serializers import game_serializer


class GameSerializer(game_serializer.GameSerializer):
    def to_representation(self, instance):
        result = super().to_representation(instance)
        self._get_current_move(result)
        return result

    def _get_current_move(self, result):
        result["current_move"] = result.pop("moves")[-1]


class PlayerGamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ["games"]

    games = GameSerializer(many=True, read_only=True)


class PlayerGamesView(RetrieveAPIView):
    permission_classes = []

    serializer_class = PlayerGamesSerializer
    queryset = Player.objects.all()
    lookup_field = "username"
