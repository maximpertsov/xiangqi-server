from rest_framework import serializers

from lib.pyffish import xiangqi
from xiangqi.models import DrawEvent, Game, TakebackEvent
from xiangqi.models.team import Team
from xiangqi.serializers.move_serializer import MoveSerializer, PositionSerializer
from xiangqi.serializers.player_serializer import PlayerSerializer


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = [
            "slug",
            "moves",
            "player1",
            "red_score",
            "player2",
            "black_score",
        ]

    moves = MoveSerializer(source="move_set", many=True, read_only=True)
    player1 = PlayerSerializer(read_only=True)
    player2 = PlayerSerializer(read_only=True)

    def to_representation(self, instance):
        result = super().to_representation(instance)
        self._transform_moves(result)
        self._transform_players(result)
        self._add_open_draw_offer(result, instance)
        self._add_open_takeback_offer(result, instance)
        return result

    def _transform_moves(self, result):
        start_position = PositionSerializer(data={"fen": xiangqi.start_fen()})
        start_position.is_valid(raise_exception=True)
        result["moves"] = [start_position.data] + result["moves"]

    def _transform_players(self, result):
        result["player1"]["team"] = Team.RED.value
        result["player2"]["team"] = Team.BLACK.value

    def _add_open_draw_offer(self, result, instance):
        result["open_draw_offer"] = None

        first_open_offer = (
            DrawEvent.open_offers.filter(game=instance).order_by("created_at").first()
        )
        if first_open_offer:
            result["open_draw_offer"] = first_open_offer.payload["username"]

    def _add_open_takeback_offer(self, result, instance):
        result["open_takeback_offer"] = None

        first_open_offer = (
            TakebackEvent.open_offers.filter(game=instance).order_by("created_at").first()
        )
        if first_open_offer:
            result["open_takeback_offer"] = first_open_offer.payload["username"]
