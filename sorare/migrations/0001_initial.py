# Generated by Django 3.0.5 on 2023-01-31 19:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ScoutingResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=200)),
                ('lastName', models.CharField(max_length=200)),
                ('playerSlug', models.CharField(db_index=True, max_length=200)),
                ('initialSO5average15', models.DecimalField(decimal_places=1, max_digits=4)),
                ('initialFifthLastScore', models.DecimalField(decimal_places=1, max_digits=4)),
                ('league', models.CharField(max_length=50)),
                ('position', models.CharField(max_length=50)),
                ('initialFloorPriceLimitedETH', models.DecimalField(decimal_places=2, max_digits=7)),
                ('initialFloorPriceLimitedEUR', models.DecimalField(decimal_places=2, max_digits=7)),
                ('created', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='FloorPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('floorPriceETH', models.DecimalField(decimal_places=2, max_digits=7)),
                ('floorPriceEUR', models.DecimalField(decimal_places=2, max_digits=7)),
                ('created', models.DateField(auto_now_add=True)),
                ('scouting_result', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='sorare.ScoutingResult')),
            ],
        ),
    ]