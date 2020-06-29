from rest_framework import serializers

from xiangqi.models import GameRequest, Player


class GameRequestSerializer(serializers.ModelSerializer):
    players = serializers.SlugRelatedField(
        "username", source="player_set", queryset=Player.objects.all(), many=True
    )

    class Meta:
        model = GameRequest
        fields = ["players", "parameters", "closed_at"]

    def create(self, validated_data):
        instance = super().create(validated_data)
        # create game if necessary
        return instance


class GameRequestPlayerSerializer(serializers.ModelSerializer):
    player = serializers.SlugRelatedField("username", queryset=Player.objects.all())
    # TODO: don't expose pk
    gamerequest = serializers.PrimaryKeyRelatedField(queryset=GameRequest.objects.all())

    class Meta:
        model = GameRequest.player_set.through
        fields = ["gamerequest", "player"]
