from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from django_fsm import FSMField, post_transition, transition

from xiangqi.models import GameTransition, Player


class GameManager(models.Manager):
    def _generate_slug(self):
        size = 8
        while True:
            slug = get_random_string(size).lower()
            if self.filter(slug=slug).exists():
                size += 1
                continue
            return slug

    def create(self, slug=None, **kwargs):
        kwargs["slug"] = self._generate_slug() if slug is None else slug
        # TODO: save initial transition
        return super().create(**kwargs)

    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class Game(models.Model):
    class NoTransition(Exception):
        pass

    class TransitionError(Exception):
        pass

    class State:
        RED_TURN = "red_turn"
        BLACK_TURN = "black_turn"
        ABORTED = "aborted"
        GAME_OVER = "game_over"

    objects = GameManager()

    state = FSMField(default=State.RED_TURN)

    slug = models.CharField(max_length=64, unique=True, editable=False)
    # TODO validate that red_player != black_player
    red_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="+")
    black_player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="+")

    def natural_key(self):
        return self.slug

    def __str__(self):
        return self.slug

    def clean(self):
        if self.red_player == self.black_player:
            raise ValidationError("Red and black players cannot be the same")

    # Transitions

    # TODO: move into abstract state model?
    def shuttle(self, event):
        transition_count = 0
        for available_transition in self.get_available_state_transitions():
            try:
                getattr(self, available_transition.name)(event)
                transition_count += 1
            except self.NoTransition:
                pass

        if not transition_count:
            raise self.TransitionError

    @transition(field=state, source=State.RED_TURN, target=State.BLACK_TURN)
    @transition(field=state, source=State.BLACK_TURN, target=State.RED_TURN)
    def change_turn(self, event):
        if event.name != "move":
            raise self.NoTransition


@receiver(post_transition, sender=Game)
def save_transition(sender, instance, target, method_args, **kwargs):
    (event,) = method_args
    with transaction.atomic():
        instance.save()
        GameTransition.objects.create(
            game=instance, to_state=target, casual_event=event
        )
