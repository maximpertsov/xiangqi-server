from rest_framework import serializers

from xiangqi.models import Game, Move
from xiangqi.serializers.move_serializer import MoveSerializer


class GameSerializer(serializers.ModelSerializer):
    moves = MoveSerializer(source="move_set", many=True, read_only=True)

    class Meta:
        model = Game
        fields = ["slug", "moves"]
