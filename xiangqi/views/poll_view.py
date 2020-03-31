from django.http import JsonResponse
from django.views.generic.detail import View

from xiangqi.views.game_mixin import GameMixin


class PollView(GameMixin, View):
    def get(self, request, slug):
        return JsonResponse({"update_count": self._transition_count}, status=200)

    @property
    def _transition_count(self):
        return self.game.transition_set.count()
