from rest_framework.serializers import ModelSerializer

from xiangqi.models import Move, Player


class PlayerSerializer(ModelSerializer):
    class Meta:
        model = Player
        fields = ["username"]


class MoveSerializer(ModelSerializer):
    class Meta:
        model = Move
        fields = ["game", "name", "player"]

    player = PlayerSerializer()

    def to_representation(self, instance):
        # TODO: add fen/gives_check/legal_moves data
        pass
