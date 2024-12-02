from datetime import timedelta
from django.test import TestCase
from unittest.mock import patch, MagicMock
from tasks.repositories.filter_repo import FilterRepo
from tasks.models import Task
from django.utils import timezone
import uuid

class TestFilterRepo(TestCase):
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


    @patch('tasks.models.Task.objects.filter')
    def test_filter_tasks_by_assignee(self, mock_filter):
        assignee = "Rafi"
        mock_filter.return_value = [task for task in self.task_repository if task.assignee == assignee]
        tasks = FilterRepo.filter_tasks(cycle_id='test',assignee_username=assignee)
        self.assertEqual(tasks, mock_filter.return_value)

    @patch('tasks.models.Task.objects.filter')
    def test_filter_tasks_by_period(self, mock_filter):
        period = "today"
        mock_filter.return_value = [task for task in self.task_repository if task.date == timezone.now().date()]
        tasks = FilterRepo.filter_tasks(cycle_id='test', period=period)
        self.assertEqual(tasks, mock_filter.return_value)

    @patch('tasks.models.Task.objects.filter')
    def test_filter_tasks_by_period_past(self, mock_filter):
        period = "past"
        mock_filter.return_value = [task for task in self.task_repository if task.date < timezone.now().date()]
        tasks = FilterRepo.filter_tasks(cycle_id='test', period=period)
        self.assertEqual(tasks, mock_filter.return_value)

    @patch('tasks.models.Task.objects.filter')
    def test_filter_tasks_by_period_upcoming(self, mock_filter):
        period = "upcoming"
        mock_filter.return_value = [task for task in self.task_repository if task.date > timezone.now().date()]
        tasks = FilterRepo.filter_tasks(cycle_id='test', period=period)
        self.assertEqual(tasks, mock_filter.return_value)

    @patch('tasks.models.Task.objects.filter')
    def test_filter_tasks_by_assignee_and_period(self, mock_filter):
        assignee = "Rafi"
        period = "today"
        mock_filter.return_value = [task for task in self.task_repository if task.assignee == assignee and task.date == timezone.now().date()]
        tasks = FilterRepo.filter_tasks(cycle_id='test', assignee_username=assignee, period=period)
        self.assertEqual(tasks, mock_filter.return_value)

