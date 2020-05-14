from rest_framework.serializers import ModelSerializer, SlugRelatedField

from xiangqi.lib.pyffish import xiangqi
from xiangqi.models import Move


class MoveSerializer(ModelSerializer):
    game = SlugRelatedField(read_only=True, slug_field="slug")
    player = SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        model = Move
        fields = ["game", "name", "player"]

    def to_representation(self, instance):
        result = super().to_representation(instance)
        if instance.previous_move:
            args = [instance.previous_move.fen, [instance.name]]
            result.update(
                fen=xiangqi.get_fen(*args),
                gives_check=xiangqi.gives_check(*args),
                legal_moves=xiangqi.legal_moves(*args),
            )
        return result
