# Generated by Django 2.2 on 2019-06-25 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xiangqi', '0014_auto_20190624_0305'),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('string', models.CharField(max_length=255, unique=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('expires_in', models.PositiveIntegerField(default=3600, help_text='In seconds', null=True)),
            ],
        ),
    ]
