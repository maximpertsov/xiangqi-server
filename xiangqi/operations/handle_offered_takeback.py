from django.utils.functional import cached_property


class HandleOfferedTakeback:
    def perform(self, event):
        self._event = event

        self._associate_with_last_move()

    def _associate_with_last_move(self):
        if not self._move_to_take_back:
            return

        self._move_to_take_back.event_set.add(self._event)

    @cached_property
    def _move_to_take_back(self):
        return (
            self._game.move_set.filter(player__username=self._username)
            .order_by("-pk")
            .first()
        )

    @property
    def _game(self):
        return self._event.game

    @property
    def _username(self):
        return self._event.payload["username"]
