# Generated by Django 2.2 on 2020-05-11 12:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('xiangqi', '0003_auto_20200507_0132'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='state',
        ),
    ]
