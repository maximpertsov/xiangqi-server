from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.utils.functional import cached_property
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.detail import SingleObjectMixin, View
from rest_framework import serializers

from xiangqi.models import Game, Player
from xiangqi.serializers.move_serializer import MoveSerializer


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ["slug", "moves"]

    moves = MoveSerializer(source="move_set", many=True, read_only=True)

    def to_representation(self, instance):
        result = super().to_representation(instance)
        self._get_current_move(result)
        return result

    def _get_current_move(result):
        result["move"] = result.pop("moves")[-1]


class GameListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ["games"]

    games = GameSerializer(many=True, read_only=True)


@method_decorator(ensure_csrf_cookie, name="dispatch")
class GameListView(SingleObjectMixin, View):
    model = Player
    slug_field = "username"
    slug_url_kwarg = "username"

    def get(self, request, username):
        return JsonResponse({"games": list(self._games_data)}, status=200)

    @property
    def _games_data(self):
        for game in self._games:
            yield {"slug": game.slug}

    @cached_property
    def _games(self):
        return self._player.games

    @property
    def _player(self):
        return self.get_object()
