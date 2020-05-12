from rest_framework.serializers import ModelSerializer

from xiangqi.models import Move

from .player_serializer import PlayerSerializer


class MoveSerializer(ModelSerializer):
    class Meta:
        model = Move
        fields = ["game", "name", "player"]

    player = PlayerSerializer()

    def to_representation(self, instance):
        # TODO: add fen/gives_check/legal_moves data
        pass
