# Generated by Django 3.0.5 on 2020-05-04 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allstar_teams', '0005_auto_20200503_2024'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='slug',
            field=models.SlugField(default='player', max_length=200),
            preserve_default=False,
        ),
    ]
