from django.utils import timezone
from django.utils.functional import cached_property


class HandleResigned:
    def perform(self, event):
        self._event = event

        self._set_game_result()

    def _set_game_result(self):
        if sum(self._scores):
            self._game.score1, self._game.score2 = self._scores
            self._game.finished_at = timezone.now()
            self._game.save()

    @cached_property
    def _scores(self):
        if self._payload["username"] == self._game.player1.username:
            return [0.0, 1.0]
        if self._payload["username"] == self._game.player2.username:
            return [1.0, 0.0]
        return [0.0, 0.0]

    @property
    def _payload(self):
        return self._event.payload

    @property
    def _game(self):
        return self._event.game
