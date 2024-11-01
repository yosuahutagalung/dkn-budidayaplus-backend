from django.db import models
from pond.models import Pond
from django.contrib.auth.models import User
import uuid

class Cycle(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('STOPPED', 'Stopped'),
        ('COMPLETED', 'Completed')
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start_date = models.DateField()
    end_date = models.DateField()
    supervisor = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    
    def stop(self):
        self.status = 'STOPPED'
        self.end_date = date.today()
        self.save()

    
class PondFishAmount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE, related_name='pond_fish_amount')
    pond = models.ForeignKey(Pond, on_delete=models.CASCADE)
    fish_amount = models.IntegerField()
