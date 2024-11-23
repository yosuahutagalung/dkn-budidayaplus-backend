from django.test import TestCase
from unittest.mock import patch, MagicMock
from tasks.models import Task
from django.utils import timezone
from datetime import timedelta
from tasks.services.filter_service_impl import FilterServiceImpl
import uuid


class TestFilterService(TestCase):
    def setUp(self):
        self.task1 = MagicMock(Task)
        self.task1.id = uuid.uuid4()
        self.task1.assignee = "Rafi"
        self.task1.date = timezone.now().date() - timedelta(days=1)

        self.task2 = MagicMock(Task)
        self.task2.id = uuid.uuid4()
        self.task2.assignee = "Rafi"
        self.task2.date = timezone.now().date()

        self.task3 = MagicMock(Task)
        self.task3.id = uuid.uuid4()
        self.task3.assignee = "Rafi"
        self.task3.date = timezone.now().date() + timedelta(days=1)

        self.task4 = MagicMock(Task)
        self.task4.id = uuid.uuid4()
        self.task4.assignee = "Rafli"
        self.task4.date = timezone.now().date() + timedelta(days=1)

        self.task_repository = [self.task1, self.task2, self.task3, self.task4]


    @patch('tasks.repositories.filter_repo.FilterRepo.filter_tasks')
    def test_filter_tasks(self, mock_filter):
        mock_filter.return_value = [task for task in self.task_repository if task.assignee == "Rafi"]
        tasks = FilterServiceImpl.filter_tasks(cycle_id='1', assignee_username="Rafi")
        self.assertEqual(tasks, mock_filter.return_value)

