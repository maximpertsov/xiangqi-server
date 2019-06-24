from django.db import models


class MoveType(models.Model):
    name = models.CharField(max_length=64)
