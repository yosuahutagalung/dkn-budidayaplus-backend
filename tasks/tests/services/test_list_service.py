from django.test import TestCase
from unittest.mock import patch, MagicMock
from tasks.services.list_service_impl import ListServiceImpl
from tasks.models import Task
import uuid

class ListServiceImplTest(TestCase):

    def test_list_tasks(self):
        with patch('tasks.repositories.list_repo.ListRepo.list_tasks') as mock_list_tasks:
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

    def test_list_tasks_empty(self):
        with patch('tasks.repositories.list_repo.ListRepo.list_tasks') as mock_list_tasks:
            cycle_id = uuid.uuid4() 
            mock_list_tasks.return_value = []

            tasks = ListServiceImpl.list_tasks(cycle_id=cycle_id)

            self.assertEqual(len(tasks), 0)

    def test_list_tasks_sorted_date(self):
        with patch('tasks.repositories.list_repo.ListRepo.list_upcoming_tasks') as mock_list_upcoming_tasks, \
            patch('tasks.repositories.list_repo.ListRepo.list_past_tasks') as mock_list_past_tasks:
            cycle_id = uuid.uuid4() 

            task_1 = MagicMock(spec=Task)
            task_1.id = uuid.uuid4()

            task_2 = MagicMock(spec=Task)
            task_2.id = uuid.uuid4()

            mock_list_upcoming_tasks.return_value = [task_1]
            mock_list_past_tasks.return_value = [task_2]

            tasks = ListServiceImpl.list_tasks_sorted_date(cycle_id=cycle_id)

            self.assertEqual(len(tasks["upcoming"]), 1)
            self.assertEqual(tasks["upcoming"][0].id, task_1.id)

            self.assertEqual(len(tasks["past"]), 1)
            self.assertEqual(tasks["past"][0].id, task_2.id)