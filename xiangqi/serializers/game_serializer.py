from rest_framework.serializers import ModelSerializer

from xiangqi.models import Game

from xiangqi.serializers.move_serializer import MoveSerializer


class GameSerializer(ModelSerializer):
    moves = MoveSerializer(source="move_set", read_only=True, many=True)


    class Meta:
        model = Game
        fields = ["moves", "slug"]

    # def to_representation(self, instance):
    #     result = super().to_representation(instance)
    #     if instance.previous_move:
    #         args = [instance.previous_move.fen, [instance.name]]
    #         result.update(
    #             fen=xiangqi.get_fen(*args),
    #             gives_check=xiangqi.gives_check(*args),
    #             legal_moves=xiangqi.legal_moves(*args),
    #         )
    #     return result
