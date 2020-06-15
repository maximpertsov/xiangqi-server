from django.contrib.postgres.fields.jsonb import JSONField
from django.core.cache import cache
from django.db import models
from django.utils.timezone import datetime

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


class UnresolvedEventQuerySet(models.QuerySet):
    def __init__(self, *args, open_events=None, close_events=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._open_events = open_events or []
        self._close_events = close_events or []

    def open(self):
        return self.filter(
            name__in=self._open_events,
            created_at__gt=models.Subquery(self._last_close_event_datetime()),
        )

    def _last_close_event_datetime(self):
        return (
            self.filter(game=models.OuterRef("game"), name__in=self._all_events())
            .annotate(
                _created_at=models.Case(
                    models.When(name__in=self._open_events, then=datetime.min),
                    default=models.F("created_at"),
                )
            )
            .values("game")
            .annotate(result=models.Max("_created_at"))
            .values("result")[:1]
        )

    def _all_events(self):
        return self._open_events + self._close_events


class GameEvent(models.Model):
    class Meta:
        indexes = [models.Index(fields=["name", "created_at"])]

    objects = GameEventManager()

    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=128)
    game = models.ForeignKey("game", related_name="event_set", on_delete=models.CASCADE)
    payload = JSONField()
