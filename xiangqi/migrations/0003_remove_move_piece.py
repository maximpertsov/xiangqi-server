# Generated by Django 2.2 on 2019-11-28 20:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('xiangqi', '0002_auto_20191128_1850'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='move',
            name='piece',
        ),
    ]