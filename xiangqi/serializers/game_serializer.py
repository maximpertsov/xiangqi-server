from rest_framework import serializers

from xiangqi.models import Game
from xiangqi.models.color import Color
from xiangqi.serializers.move_serializer import MoveSerializer
from xiangqi.serializers.player_serializer import PlayerSerializer


class GameSerializer(serializers.ModelSerializer):
    moves = MoveSerializer(source="move_set", many=True, read_only=True)
    red_player = PlayerSerializer(read_only=True)
    black_player = PlayerSerializer(read_only=True)

    def to_representation(self, instance):
        result = super().to_representation(instance)
        # TODO: update client expect `.red_player` and `.black_player` keys,
        # instance of a list of players
        result["red_player"].update(color=Color.RED.value)
        result["black_player"].update(color=Color.BLACK.value)
        result["players"] = [result.pop("red_player"), result.pop("black_player")]
        return result

    class Meta:
        model = Game
        fields = ["moves", "red_player", "black_player"]
