# Generated by Django 2.2 on 2020-03-31 16:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('xiangqi', '0025_auto_20200331_1259'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='participants',
        ),
    ]