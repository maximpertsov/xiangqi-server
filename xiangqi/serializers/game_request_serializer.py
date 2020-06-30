from random import shuffle

from rest_framework import serializers

from xiangqi.models import GameRequest, Player
from xiangqi.models.team import Team
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
        game = GameSerializer(data=self._game_players(instance))
        game.is_valid(raise_exception=True)
        game.save()

    def _game_players(self, instance):
        players = [instance.player1, instance.player2]
        team = instance.parameters.get("team")

        if team == Team.RED.value:
            pass
        elif team == Team.BLACK.value:
            players.reverse()
        else:
            shuffle(players)

        return dict(zip(["player1", "player2"], players))
