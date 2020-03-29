from django.db import models


class GameTransition(models.Model):
    game = models.ForeignKey("game", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    to_state = models.CharField(max_length=50)
    casual_event = models.ForeignKey(
        "gameevent", on_delete=models.SET_NULL, related_name="transition_set", null=True
    )
