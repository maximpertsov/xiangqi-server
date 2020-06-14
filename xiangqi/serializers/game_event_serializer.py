import importlib

from rest_framework import serializers

from xiangqi.models import Game, GameEvent


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
            handler = self._get_handler_class(event)
            handler().perform(event=event)
        except (AttributeError, ModuleNotFoundError):
            return

    @staticmethod
    def _get_handler_class(event):
        handler_name = "handle_{}".format(event.name)
        return getattr(
            importlib.import_module("xiangqi.operations.{}".format(handler_name)),
            handler_name.title().replace("_", ""),
        )
