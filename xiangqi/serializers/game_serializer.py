from rest_framework import serializers

from lib.pyffish import xiangqi
from xiangqi.models import Game
from xiangqi.models.color import Color
from xiangqi.serializers.move_serializer import MoveSerializer, PositionSerializer
from xiangqi.serializers.player_serializer import PlayerSerializer


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = [
            "slug",
            "moves",
            "red_player",
            "red_score",
            "black_player",
            "black_score",
        ]

    moves = MoveSerializer(source="move_set", many=True, read_only=True)
    red_player = PlayerSerializer(read_only=True)
    black_player = PlayerSerializer(read_only=True)

    def to_representation(self, instance):
        result = super().to_representation(instance)
        self._transform_moves(result)
        self._transform_players(result)
        return result

    def _transform_moves(self, result):
        start_position = PositionSerializer(data={"fen": xiangqi.start_fen()})
        start_position.is_valid(raise_exception=True)
        result["moves"] = [start_position.data] + result["moves"]

    def _transform_players(self, result):
        result["red_player"]["color"] = Color.RED.value
        result["black_player"]["color"] = Color.BLACK.value
