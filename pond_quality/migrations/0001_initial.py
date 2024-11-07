import django.core.validators
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cycle', '0001_initial'),
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
                ('ph_level', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(14.0)])),
                ('salinity', models.FloatField()),
                ('water_temperature', models.FloatField()),
                ('water_clarity', models.FloatField()),
                ('water_circulation', models.FloatField()),
                ('dissolved_oxygen', models.FloatField()),
                ('orp', models.FloatField()),
                ('ammonia', models.FloatField()),
                ('nitrate', models.FloatField()),
                ('phosphate', models.FloatField()),
                ('cycle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cycle.cycle')),
                ('pond', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pond.pond')),
                ('reporter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
