from rest_framework import serializers

from lib.pyffish import xiangqi
from xiangqi.models import Game, Move, Player
from xiangqi.queries.legal_moves import LegalMoves


class MoveSerializer(serializers.ModelSerializer):
    game = serializers.SlugRelatedField(
        "slug", write_only=True, queryset=Game.objects.all()
    )
    player = serializers.SlugRelatedField("username", queryset=Player.objects.all())

    def to_representation(self, instance):
        result = super().to_representation(instance)
        result.update(
            gives_check=xiangqi.gives_check(instance.fen, []),
            legal_moves=LegalMoves(fen=instance.fen).result(),
        )
        return result

    class Meta:
        model = Move
        fields = ["fan", "fen", "game", "player"]
