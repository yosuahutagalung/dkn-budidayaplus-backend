# Generated by Django 5.1.2 on 2024-10-15 16:36

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cycle', '0004_rename_cyclefishdistribution_pondfishamount'),
        ('pond', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodSampling',
            fields=[
                ('sampling_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('food_quantity', models.IntegerField()),
                ('sample_date', models.DateField()),
                ('cycle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cycle.cycle')),
                ('pond', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pond.pond')),
                ('reporter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]