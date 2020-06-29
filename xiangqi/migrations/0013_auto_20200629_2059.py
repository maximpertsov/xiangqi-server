# Generated by Django 3.0.7 on 2020-06-29 20:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('xiangqi', '0012_auto_20200629_2012'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gamerequest',
            name='player_set',
        ),
        migrations.AddField(
            model_name='gamerequest',
            name='player',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='xiangqi.Player'),
            preserve_default=False,
        ),
    ]
