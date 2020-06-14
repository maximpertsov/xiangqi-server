from rest_framework import serializers

from xiangqi.models import Game, GameEvent
from xiangqi.models.draw_event import DrawEventTypes
from xiangqi.models.takeback_event import TakebackEventTypes
from xiangqi.operations.create_move import CreateMove
from xiangqi.operations.handle_accepted_draw import HandleAcceptedDraw
from xiangqi.operations.handle_offered_takeback import HandleOfferedTakeback
from xiangqi.operations.handle_resigned import HandleResigned

EVENT_HANDLER_CLASSES = {
    "move": CreateMove,
    DrawEventTypes.ACCEPTED_DRAW.value: HandleAcceptedDraw,
    TakebackEventTypes.OFFERED_TAKEBACK.value: HandleOfferedTakeback,
    "resigned": HandleResigned,
}


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
            handler().perform(event=event)
        except KeyError:
            return
