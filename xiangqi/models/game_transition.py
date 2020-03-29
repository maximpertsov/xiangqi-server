from django.core.cache import cache
from django.db import models

CACHE_TTL = None


def get_cache_key(game_slug):
    return "transition_count_{}".format(game_slug)


class GameTransitionManager(models.Manager):
    def create(self, **kwargs):
        instance = super().create(**kwargs)
        cache.delete(get_cache_key(instance.game.slug))
        return instance

    def count(self, **kwargs):
        game = self.core_filters["game"]
        if not game:
            return super().count(**kwargs)

        cache_key = get_cache_key(game.slug)
        result = cache.get(cache_key)
        if result is None:
            result = super().count(**kwargs)
            cache.set(cache_key, result, timeout=CACHE_TTL)

        return result


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
