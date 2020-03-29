from django.core.cache import cache
from django.db import models


def get_cache_key(game_slug):
    return "transition_count_{}".format(game_slug)


class GameTransitionManager(models.Manager):
    def create(self, **kwargs):
        instance = super().create(**kwargs)
        cache.delete(get_cache_key(instance.game.slug))
        return instance


class GameTransition(models.Model):
    objects = GameTransitionManager()

    game = models.ForeignKey(
        "game", on_delete=models.CASCADE, related_name="transition_set"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    to_state = models.CharField(max_length=50)
    casual_event = models.ForeignKey(
        "gameevent", on_delete=models.SET_NULL, related_name="transition_set", null=True
    )
