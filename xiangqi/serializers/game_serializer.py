from collections import OrderedDict

from rest_framework import serializers

from lib.pyffish import xiangqi
from xiangqi.models import Game
from xiangqi.models.color import Color
from xiangqi.queries.legal_moves import LegalMoves
from xiangqi.serializers.move_serializer import MoveSerializer, PositionSerializer
from xiangqi.serializers.player_serializer import PlayerSerializer


class GameSerializer(serializers.ModelSerializer):
    moves = MoveSerializer(source="move_set", many=True, read_only=True)
    red_player = PlayerSerializer(read_only=True)
    black_player = PlayerSerializer(read_only=True)

    def to_representation(self, instance):
        result = super().to_representation(instance)
        self._transform_players(result)
        self._transform_moves(result)
        return result

    def _transform_players(self, result):
        # TODO: update client expect `.red_player` and `.black_player` keys,
        # instance of a list of players
        result["red_player"].update(color=Color.RED.value)
        result["black_player"].update(color=Color.BLACK.value)
        result["players"] = [result.pop("red_player"), result.pop("black_player")]

    def _transform_moves(self, result):
        # TODO: this should be it's own serializer and collocated with the move serialier
        start_position = PositionSerializer(data={"fen": xiangqi.start_fen()})
        start_position.is_valid(raise_exception=True)
        result["moves"] = [start_position.data] + result["moves"]

    class Meta:
        model = Game
        fields = ["moves", "red_player", "black_player"]
