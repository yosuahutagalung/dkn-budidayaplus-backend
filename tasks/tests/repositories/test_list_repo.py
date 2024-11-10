from django.test import TestCase
from unittest.mock import patch, MagicMock
from tasks.repositories.list_repo import ListRepo
from tasks.models import Task
from datetime import date
import uuid

class ListRepoTest(TestCase):
    @patch('tasks.models.Task.objects.filter')
    def test_list_repo(self, mock_list):
        cycle_id = uuid.uuid4()

        mock_task1 = MagicMock(spec=Task)
        mock_task1.id = uuid.uuid4()
        mock_task1.task_type = 'POND_QUALITY'
        mock_task1.date = date.today()
        mock_task1.status = 'TODO'
        mock_task1.cycle_id = cycle_id

        mock_task2 = MagicMock(spec=Task)
        mock_task2.id = uuid.uuid4()
        mock_task2.task_type = 'FISH_SAMPLING'
        mock_task2.date = date.today()
        mock_task2.status = 'TODO'
        mock_task2.cycle_id = cycle_id

        mock_task3 = MagicMock(spec=Task)
        mock_task3.id = uuid.uuid4()
        mock_task3.task_type = 'POND_QUALITY'
        mock_task3.date = date.today()
        mock_task3.status = 'TODO'
        mock_task3.cycle_id = uuid.uuid4()

        mock_task_list = [mock_task1, mock_task2, mock_task3]
        mock_list.return_value = [task for task in mock_task_list if task.cycle_id == cycle_id]

        tasks = ListRepo.list_tasks(cycle_id=cycle_id)

        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].id, mock_task1.id)
        self.assertEqual(tasks[1].id, mock_task2.id)
        self.assertEqual(tasks[0].task_type, mock_task1.task_type)
        self.assertEqual(tasks[1].task_type, mock_task2.task_type)
