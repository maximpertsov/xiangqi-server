# Generated by Django 2.2 on 2020-03-31 12:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('xiangqi', '0024_auto_20200329_2009'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='black_player',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='xiangqi.User'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='red_player',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='xiangqi.User'),
            preserve_default=False,
        ),
    ]