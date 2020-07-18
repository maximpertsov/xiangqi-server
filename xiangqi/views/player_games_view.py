from rest_framework import serializers
from rest_framework.generics import RetrieveAPIView

from xiangqi.models import Game, Player
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

    games = GameSerializer(source="active_games", many=True, read_only=True)


class PlayerGamesView(RetrieveAPIView):
    serializer_class = PlayerGamesSerializer
    queryset = Player.objects.all()
    lookup_field = "username"
