from rest_framework import serializers

from lib.pyffish import xiangqi
from xiangqi.models import Game, Move, Player
from xiangqi.queries.game_result import GameResult
from xiangqi.queries.legal_moves import LegalMoves


class PositionSerializer(serializers.Serializer):
    fen = serializers.CharField()

    def to_representation(self, instance):
        result = super().to_representation(instance)
        result.update(
            gives_check=xiangqi.gives_check(result["fen"], []),
            legal_moves=LegalMoves(fen=result["fen"]).result,
            game_result=GameResult().result(move=instance),
        )
        return result


class MoveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Move
        fields = ["uci", "fen", "game", "player"]

    game = serializers.SlugRelatedField(
        "slug", write_only=True, queryset=Game.objects.all()
    )
    player = serializers.SlugRelatedField("username", queryset=Player.objects.all())

    def to_representation(self, instance):
        result = super().to_representation(instance)
        position = PositionSerializer(data={"fen": instance.fen})
        position.is_valid(raise_exception=True)
        result.update(position.data)
        return result
