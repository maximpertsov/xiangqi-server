from rest_framework import serializers

from xiangqi.models import Game, Move, Player


class MoveSerializer(serializers.ModelSerializer):
    game = serializers.SlugRelatedField("slug", queryset=Game.objects.all())
    player = serializers.SlugRelatedField("username", queryset=Player.objects.all())

    # def validate(self, data):
    #     game = (
    #         Game.objects.filter(slug=data["game"])
    #         .select_related("red_player", "black_player")
    #         .first()
    #     )
    #     if data["player"] not in [game.red_player.username, game.black_player.username]:
    #         raise serializers.ValidationError("Move made by non-game player")
    #     return data

    class Meta:
        model = Move
        fields = ["fan", "fen", "game", "player"]
