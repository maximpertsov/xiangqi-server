import json
from functools import partial

from django.core import serializers
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import ListView

from xiangqi.models.game import Game

serialize = partial(serializers.serialize, "json", use_natural_foreign_keys=True)


@method_decorator(ensure_csrf_cookie, name="dispatch")
class GameListView(ListView):
    model = Game

    def get(self, request, username):
        queryset = self.get_queryset().filter(
            participant__player__user__username=username
        )
        serialized = serialize(queryset)
        games = [{"slug": data["fields"]["slug"]} for data in json.loads(serialized)]
        return JsonResponse({"games": games}, status=200)
