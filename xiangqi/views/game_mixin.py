from django.views.generic.detail import SingleObjectMixin

from xiangqi.models.game import Game


class GameMixin(SingleObjectMixin):
    model = Game

    @property
    def game(self):
        return self.get_object()
