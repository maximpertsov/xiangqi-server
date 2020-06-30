from rest_framework import serializers

from xiangqi.models import GameRequest, Player
from xiangqi.serializers.game_serializer import GameSerializer


class GameRequestSerializer(serializers.ModelSerializer):
    player1 = serializers.SlugRelatedField("username", queryset=Player.objects.all())
    player2 = serializers.SlugRelatedField(
        "username", queryset=Player.objects.all(), required=False
    )

    class Meta:
        model = GameRequest
        fields = ["id", "player1", "player2", "parameters"]

    def update(self, instance, validated_data):
        updated_instance = super().update(instance, validated_data)
        if updated_instance.player1 and updated_instance.player2:
            self._create_game(updated_instance)
        return updated_instance

    def _create_game(self, instance):
        game = GameSerializer(
            data={
                "player1": instance.player1.username,
                "player2": instance.player2.username,
            }
        )
        game.is_valid(raise_exception=True)
        game.save()
