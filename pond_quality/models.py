from django.db import models
from pond.models import Pond
from cycle.models import Cycle
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid

class PondQuality(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pond = models.ForeignKey(Pond, on_delete=models.CASCADE)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE)
    recorded_at = models.DateTimeField(auto_now_add=True)
    image_name = models.CharField(max_length=255, blank=True)
    ph_level = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(14.0)])
    salinity = models.FloatField()
    water_temperature = models.FloatField()
    water_clarity = models.FloatField()
    water_circulation = models.FloatField()
    dissolved_oxygen = models.FloatField()
    orp = models.FloatField()
    ammonia = models.FloatField()
    nitrate = models.FloatField()
    phosphate = models.FloatField()

    def __str__(self):
        return str(self.id)