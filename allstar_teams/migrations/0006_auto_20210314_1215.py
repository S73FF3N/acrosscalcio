# Generated by Django 3.0.5 on 2021-03-14 12:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('allstar_teams', '0005_person'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='birth_date',
            field=models.DateField(default=datetime.date(1969, 10, 19)),
        ),
    ]