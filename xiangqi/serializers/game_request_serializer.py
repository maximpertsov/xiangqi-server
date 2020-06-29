from rest_framework import serializers

from xiangqi.models import GameRequest, Player


class GameRequestSerializer(serializers.ModelSerializer):
    player1 = serializers.SlugRelatedField("username", queryset=Player.objects.all())
    player2 = serializers.SlugRelatedField(
        "username", queryset=Player.objects.all(), required=False
    )

    class Meta:
        model = GameRequest
        fields = ["player1", "player2", "parameters"]
