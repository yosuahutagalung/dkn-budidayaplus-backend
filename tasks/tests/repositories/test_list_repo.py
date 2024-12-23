from django.test import TestCase
from unittest.mock import patch, MagicMock
from tasks.repositories.list_repo import ListRepo
from tasks.models import Task
from django.utils import timezone
import uuid

class ListRepoTest(TestCase):
    def setUp(self):
        self.cycle_id = uuid.uuid4()

        self.mock_task1 = MagicMock(spec=Task)
        self.mock_task1.id = uuid.uuid4()
        self.mock_task1.task_type = 'POND_QUALITY'
        self.mock_task1.date = timezone.now().date()
        self.mock_task1.status = 'TODO'
        self.mock_task1.cycle_id = self.cycle_id

        self.mock_task2 = MagicMock(spec=Task)
        self.mock_task2.id = uuid.uuid4()
        self.mock_task2.task_type = 'FISH_SAMPLING'
        self.mock_task2.date = timezone.now().date() + timezone.timedelta(days=1)
        self.mock_task2.status = 'TODO'
        self.mock_task2.cycle_id = self.cycle_id

        self.mock_task3 = MagicMock(spec=Task)
        self.mock_task3.id = uuid.uuid4()
        self.mock_task3.task_type = 'FOOD_SAMPLING'
        self.mock_task3.date = timezone.now().date() - timezone.timedelta(days=1)
        self.mock_task3.status = 'TODO'
        self.mock_task3.cycle_id = self.cycle_id

        self.mock_task4 = MagicMock(spec=Task)
        self.mock_task4.id = uuid.uuid4()
        self.mock_task4.task_type = 'POND_QUALITY'
        self.mock_task4.date = timezone.now().date()
        self.mock_task4.status = 'TODO'
        self.mock_task4.cycle_id = uuid.uuid4()

        self.mock_task_list = [self.mock_task1, self.mock_task2, self.mock_task3, self.mock_task4]


    @patch('tasks.models.Task.objects.filter')
    def test_list_repo(self, mock_list):
        mock_list.return_value = [task for task in self.mock_task_list if task.cycle_id == self.cycle_id]

        tasks = ListRepo.list_tasks(cycle_id=self.cycle_id)

        self.assertEqual(len(tasks), 3)
        self.assertEqual(tasks[0].id, self.mock_task1.id)
        self.assertEqual(tasks[1].id, self.mock_task2.id)
        self.assertEqual(tasks[2].id, self.mock_task3.id)
        self.assertEqual(tasks[0].task_type, self.mock_task1.task_type)
        self.assertEqual(tasks[1].task_type, self.mock_task2.task_type)
        self.assertEqual(tasks[2].task_type, self.mock_task3.task_type)
        self.assertNotIn(self.mock_task4, tasks)

    @patch('tasks.models.Task.objects.filter') 
    def test_list_past_tasks(self, mock_list):
        mock_list.return_value = [task for task in self.mock_task_list if task.cycle_id == self.cycle_id and task.date < timezone.now().date()]

        tasks = ListRepo.list_past_tasks(cycle_id=self.cycle_id)

        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].id, self.mock_task3.id)
        self.assertNotIn(self.mock_task1, tasks)
        self.assertNotIn(self.mock_task2, tasks)
        self.assertNotIn(self.mock_task4, tasks)


    @patch('tasks.models.Task.objects.filter')
    def test_list_upcoming_tasks(self, mock_list):
        mock_list.return_value = [task for task in self.mock_task_list if task.cycle_id == self.cycle_id and task.date >= timezone.now().date()]

        tasks = ListRepo.list_upcoming_tasks(cycle_id=self.cycle_id)

        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].id, self.mock_task1.id)
        self.assertEqual(tasks[1].id, self.mock_task2.id)
        self.assertEqual(tasks[0].task_type, self.mock_task1.task_type)
        self.assertEqual(tasks[1].task_type, self.mock_task2.task_type)
        self.assertNotIn(self.mock_task3, tasks)
        self.assertNotIn(self.mock_task4, tasks)
