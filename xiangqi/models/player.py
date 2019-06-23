from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Player(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()

    def natural_key(self):
        return self.user.username

    natural_key.dependencies = [get_user_model()]


@receiver(post_save, sender=get_user_model())
def create_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)


@receiver(post_save, sender=get_user_model())
def save_player(sender, instance, **kwargs):
    instance.player.save()
