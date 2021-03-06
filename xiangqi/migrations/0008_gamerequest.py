# Generated by Django 3.0.7 on 2020-06-29 23:03

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('xiangqi', '0007_auto_20200617_0429'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parameters', django.contrib.postgres.fields.jsonb.JSONField()),
                ('player1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='xiangqi.Player')),
                ('player2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='xiangqi.Player')),
            ],
        ),
    ]
