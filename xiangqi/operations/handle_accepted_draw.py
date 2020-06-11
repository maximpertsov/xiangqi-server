from django.utils import timezone


class HandleAcceptedDraw:
    def __init__(self, event):
        self._event = event

    def perform(self):
        self._game.red_score, self._game.black_score = [0.5, 0.5]
        self._game.finished_at = timezone.now()
        self._game.save()

    @property
    def _game(self):
        return self._event.game
