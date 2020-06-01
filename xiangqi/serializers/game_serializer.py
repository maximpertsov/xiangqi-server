from rest_framework import serializers

from lib.pyffish import xiangqi
from xiangqi.models import Game
from xiangqi.queries.current_move_fen import CurrentMoveFen
from xiangqi.serializers.move_serializer import MoveSerializer, PositionSerializer
from xiangqi.serializers.player_serializer import PlayerSerializer


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ["slug", "moves", "red_player", "black_player", "current_move_fen"]

    moves = MoveSerializer(source="move_set", many=True, read_only=True)
    red_player = PlayerSerializer(read_only=True)
    black_player = PlayerSerializer(read_only=True)
    current_move_fen = serializers.SerializerMethodField()

    def get_current_move_fen(self, instance):
        return CurrentMoveFen(game=instance).result

    def to_representation(self, instance):
        result = super().to_representation(instance)
        self._transform_moves(result)
        return result

    def _transform_moves(self, result):
        start_position = PositionSerializer(data={"fen": xiangqi.start_fen()})
        start_position.is_valid(raise_exception=True)
        result["moves"] = [start_position.data] + result["moves"]
