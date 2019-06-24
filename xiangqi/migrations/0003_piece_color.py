# Generated by Django 2.2 on 2019-06-22 01:06

from django.db import migrations, models
import xiangqi.models


class Migration(migrations.Migration):

    dependencies = [
        ('xiangqi', '0002_participant_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='piece',
            name='color',
            field=models.CharField(choices=[(xiangqi.models.Color('red'), 'red'), (xiangqi.models.Color('black'), 'black')], default='no color', max_length=32),
            preserve_default=False,
        ),
    ]
