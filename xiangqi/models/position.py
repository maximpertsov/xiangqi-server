from django.db import models


class PositionManager(models.Manager):
    def get_by_natural_key(self, rank, file):
        return self.get(rank=rank, file=file)


# TODO: make this immutable
class Position(models.Model):
    objects = PositionManager()

    class Meta:
        unique_together = [("rank", "file")]

    rank = models.PositiveIntegerField(db_index=True)
    file = models.PositiveIntegerField(db_index=True)

    def natural_key(self):
        return (self.rank, self.file)
