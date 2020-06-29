from rest_framework import serializers

from xiangqi.models import GameRequest, Player


class GameRequestSerializer(serializers.ModelSerializer):
    player = serializers.SlugRelatedField(
        "username", queryset=Player.objects.all(), many=True
    )

    class Meta:
        model = GameRequest
        fields = ["player", "parameters", "closed_at"]
