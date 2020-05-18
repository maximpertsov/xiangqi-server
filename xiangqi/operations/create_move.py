from xiangqi.serializers.move_serializer import MoveSerializer


class CreateMove:
    def __init__(self, event):
        self._event = event

    def perform(self):
        move = MoveSerializer(data=self._data)
        move.is_valid(raise_exception=True)
        move.save()

    @property
    def _data(self):
        return {"game": self._event.game.slug, **self._event.payload}
