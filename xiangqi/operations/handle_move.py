from django.utils.functional import cached_property

from xiangqi.queries.game_result import GameResult
from xiangqi.serializers.move_serializer import MoveSerializer


class HandleMove:
    def perform(self, event):
        self._event = event
        self._set_game_result()

    def _set_game_result(self):
        scores = self._game_result
        if sum(scores):
            self._game.finish(*scores)

    @cached_property
    def _game_result(self):
        return GameResult().result(move=self._persisted_move)

    @cached_property
    def _persisted_move(self):
        move = MoveSerializer(data=self._data)
        move.is_valid(raise_exception=True)
        return move.save()

    @property
    def _data(self):
        return {"game": self._game.slug, **self._event.payload}

    @property
    def _game(self):
        return self._event.game
