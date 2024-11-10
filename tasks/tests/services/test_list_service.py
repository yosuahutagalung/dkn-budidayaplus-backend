from django.test import TestCase
from unittest.mock import patch, MagicMock
from tasks.services.list_service_impl import ListServiceImpl
from tasks.models import Task
import uuid

class ListServiceImplTest(TestCase):

    @patch('tasks.repositories.list_repo.ListRepo.list_tasks')
    def test_list_tasks(self, mock_list_tasks):
        cycle_id = uuid.uuid4() 

        task_1 = MagicMock(spec=Task)
        task_1.id = uuid.uuid4()
        task_2 = MagicMock(spec=Task)
        task_2.id = uuid.uuid4()
        mock_list_tasks.return_value = [task_1, task_2]

        tasks = ListServiceImpl.list_tasks(cycle_id=cycle_id)

        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].id, task_1.id)
        self.assertEqual(tasks[1].id, task_2.id)

    @patch('tasks.repositories.list_repo.ListRepo.list_tasks')
    def test_list_tasks_empty(self, mock_list_tasks):
        cycle_id = uuid.uuid4() 
        mock_list_tasks.return_value = []

        tasks = ListServiceImpl.list_tasks(cycle_id=cycle_id)

        self.assertEqual(len(tasks), 0)
