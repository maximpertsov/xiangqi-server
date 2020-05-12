# Generated by Django 2.2 on 2020-05-12 13:03

import django.db.models.deletion
from django.db import migrations, models


def backfill(apps, schema_editor):
    Game = apps.get_model("xiangqi", "Game")
    games = Game.objects.prefetch_related("move_set")

    for game in games:
        sorted_moves = sorted(game.move_set.all(), key=lambda obj: obj.pk)
        for move1, move2 in zip(sorted_moves, sorted_moves[1:]):
            move2.previous_move = move1
            move2.save()


class Migration(migrations.Migration):

    dependencies = [("xiangqi", "0005_delete_gametransition")]

    operations = [
        migrations.AddField(
            model_name="move",
            name="previous_move",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="xiangqi.Move",
            ),
        ),
        migrations.RunPython(backfill, migrations.RunPython.noop),
    ]
