# Generated by Django 2.2.10 on 2020-05-17 15:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('xiangqi', '0005_delete_gametransition'),
    ]

    operations = [
        migrations.RenameField(
            model_name='move',
            old_name='name',
            new_name='fan',
        ),
    ]
