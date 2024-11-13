from django.test import TestCase
from unittest.mock import MagicMock
from tasks.models import Task, TaskTemplate
from tasks.enums import TaskStatus, TaskType
from django.utils import timezone
from tasks.schemas import TaskSchema
import uuid

class TestTaskSchemas(TestCase):
    def test_resolve_task_type(self):
        task = MagicMock(spec=Task)
        task.id = uuid.uuid4()
        task.task_type = TaskType.POND_QUALITY.value
        task.status = TaskStatus.TODO.value
        task.date = timezone.now().date()
        task.cycle_id = uuid.uuid4()
        task.assignee = ''
        
        task_serialized = TaskSchema.from_orm(task)
        
        self.assertEqual(task_serialized.task_type, 'Pond Quality')
        