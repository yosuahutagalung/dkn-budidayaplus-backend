import uuid
from django.db import models
from tasks.enums import TaskStatus, TaskType
from cycle.models import Cycle

class TaskTemplate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task_type = models.CharField(max_length=4, choices=TaskType.choices)
    day_of_culture = models.PositiveIntegerField()


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task_type = models.CharField(max_length=4, choices=TaskType.choices)
    status = models.CharField(max_length=4, choices=TaskStatus.choices, default=TaskStatus.TODO)
    date = models.DateField()
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE)
    assignee = models.CharField(max_length=13)

