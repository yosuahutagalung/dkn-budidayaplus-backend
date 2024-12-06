import uuid
from django.db import models
from pond.models import Pond
from tasks.enums import TaskStatus, TaskType
from cycle.models import Cycle

class TaskTemplate(models.Model):
    task_type = models.CharField(max_length=20, choices=TaskType.choices())
    day_of_culture = models.PositiveIntegerField()

    class Meta:
        ordering = ['day_of_culture']


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task_type = models.CharField(max_length=20, choices=TaskType.choices())
    date = models.DateField()
    status = models.CharField(max_length=4, choices=TaskStatus.choices(), default=TaskStatus.TODO.value)
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE)
    assignee = models.CharField(max_length=13, blank=True)
    pond = models.ForeignKey(Pond, on_delete=models.CASCADE, blank=True)

    class Meta:
        ordering = ['date']
