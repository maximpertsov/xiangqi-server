from rest_framework import serializers

from xiangqi.models import Game, GameEvent


class GameEventSerializer(serializers.ModelSerializer):
    game = serializers.SlugRelatedField("slug", queryset=Game.objects.all())

    class Meta:
        model = GameEvent
        fields = ["game", "payload"]
