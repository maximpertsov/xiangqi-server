from rest_framework import serializers

from xiangqi.models import Game, Move, Player


class MoveSerializer(serializers.ModelSerializer):
    game = serializers.SlugRelatedField("slug", queryset=Game.objects.all())
    player = serializers.SlugRelatedField("username", queryset=Player.objects.all())

    class Meta:
        model = Move
        fields = ["game", "name", "player"]

    # def validate(self, data):
    #     return super().validate(data)
