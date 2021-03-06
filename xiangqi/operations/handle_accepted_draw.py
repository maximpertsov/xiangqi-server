from django.utils import timezone


class HandleAcceptedDraw:
    def perform(self, event):
        self._event = event
        self._set_game_result()

    def _set_game_result(self):
        self._game.score1, self._game.score2 = [0.5, 0.5]
        self._game.finished_at = timezone.now()
        self._game.save()

    @property
    def _game(self):
        return self._event.game
