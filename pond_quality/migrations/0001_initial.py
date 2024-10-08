# Generated by Django 5.1.1 on 2024-10-01 15:56

import django.core.validators
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pond', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PondQuality',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('recorded_at', models.DateTimeField(auto_now_add=True)),
                ('image_name', models.CharField(blank=True, max_length=255)),
                ('ph_level', models.FloatField(blank=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(14.0)])),
                ('salinity', models.FloatField(blank=True)),
                ('water_temperature', models.FloatField(blank=True)),
                ('water_clarity', models.FloatField(blank=True)),
                ('water_circulation', models.FloatField(blank=True)),
                ('dissolved_oxygen', models.FloatField(blank=True)),
                ('orp', models.FloatField(blank=True)),
                ('ammonia', models.FloatField(blank=True)),
                ('nitrate', models.FloatField(blank=True)),
                ('phosphate', models.FloatField(blank=True)),
                ('pond', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pond.pond')),
                ('reporter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
