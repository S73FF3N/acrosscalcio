# Generated by Django 3.0.5 on 2020-05-04 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allstar_teams', '0006_player_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='redbubble',
            field=models.URLField(blank=True),
        ),
    ]
