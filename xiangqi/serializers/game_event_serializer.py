from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from xiangqi.models import Game, GameEvent
from xiangqi.operations.create_move import CreateMove

EVENT_HANDLER_CLASSES = {"move": CreateMove}


class GameEventSerializer(serializers.ModelSerializer):
    game = serializers.SlugRelatedField("slug", queryset=Game.objects.all())

    class Meta:
        model = GameEvent
        fields = ["game", "name", "payload"]

    def create(self, validated_data):
        event = super().create(validated_data)
        self._handle_event(event)
        return event

    def _handle_event(self, event):
        try:
            handler = EVENT_HANDLER_CLASSES[event.name]
            handler(event=event).perform()
        except KeyError as event_name:
            raise ValidationError(["Unknown event {}".format(event_name)])
