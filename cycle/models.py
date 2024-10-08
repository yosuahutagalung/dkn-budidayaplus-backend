from datetime import timedelta
from django.db import models
from django.core.exceptions import ValidationError
from pond.models import Pond
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
import uuid

class Cycle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start_date = models.DateField()
    end_date = models.DateField()
    supervisor = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def clean(self):
        super().clean()
        if self.end_date != self.start_date + timedelta(days=60):
            raise ValidationError('End date must be exactly 60 days after the start date.')

    def __str__(self):
        return str(self.id)
    

class CycleFishDistribution(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE)
    pond = models.ForeignKey(Pond, on_delete=models.CASCADE)
    fish_amount = models.IntegerField(validators=[MinValueValidator(1)])

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.id)