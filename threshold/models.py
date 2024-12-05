from django.db import models

class PondQualityThreshold(models.Model):
    min_ph = models.FloatField()
    max_ph = models.FloatField()
    min_salinity = models.FloatField()
    max_salinity = models.FloatField()
    min_temperature = models.FloatField()
    max_temperature = models.FloatField()
    min_clarity = models.FloatField()
    max_clarity = models.FloatField()
    min_circulation = models.FloatField()
    max_circulation = models.FloatField()
    min_dissolved_oxygen = models.FloatField()
    max_dissolved_oxygen = models.FloatField()
    min_orp = models.FloatField()
    max_orp = models.FloatField()
    min_ammonia = models.FloatField()
    max_ammonia = models.FloatField()
    min_nitrate = models.FloatField()
    max_nitrate = models.FloatField()
    min_phosphate = models.FloatField()
    max_phosphate = models.FloatField()

    def __str__(self):
        return "Pond Quality Threshold"