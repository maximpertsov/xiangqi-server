from django.contrib.postgres.fields.jsonb import JSONField
from django.core.cache import cache
from django.db import models

from xiangqi.models.managers.open_draw_offers_manager import OpenDrawOffersManager

CACHE_TTL = 3600


def get_cache_key(game_slug):
    return "event_count_{}".format(game_slug)


class GameEventManager(models.Manager):
    def create(self, **kwargs):
        instance = super().create(**kwargs)
        cache.delete(get_cache_key(instance.game.slug))
        return instance

    def cached_count(self, **kwargs):
        game = self.core_filters["game"]
        if not game:
            return self.count(**kwargs)

        cache_key = get_cache_key(game.slug)
        result = cache.get(cache_key)
        if result is None:
            result = self.count(**kwargs)
            cache.set(cache_key, result, timeout=CACHE_TTL)

        return result


class GameEvent(models.Model):
    class Meta:
        indexes = [models.Index(fields=["name", "created_at"])]

    objects = GameEventManager()
    open_draw_offers = OpenDrawOffersManager()

    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=128)
    game = models.ForeignKey("game", related_name="event_set", on_delete=models.CASCADE)
    payload = JSONField()
