# Generated by Django 3.0.7 on 2020-06-29 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xiangqi', '0011_auto_20200629_1802'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gamerequest',
            name='player_set',
        ),
        migrations.AddField(
            model_name='gamerequest',
            name='players',
            field=models.ManyToManyField(to='xiangqi.Player'),
        ),
    ]
