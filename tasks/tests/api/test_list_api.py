from unittest.mock import patch, MagicMock
from django.test import TestCase
from tasks.models import Task
from datetime import date, timedelta
from cycle.models import Cycle
from django.http import HttpRequest
from django.contrib.auth.models import User
from tasks.api import list_tasks
from ninja.errors import HttpError
import uuid

class TaskAPITest(TestCase):
    def setUp(self):
        self.request = MagicMock(spec=HttpRequest)
        self.request.auth = MagicMock(spec=User)

        self.cycle = MagicMock(spec=Cycle)
        self.cycle.id = uuid.uuid4()
        self.start_date = date.today()
        self.end_date = date.today() + timedelta(days=60)

        self.task = MagicMock(spec=Task)
        self.task.id = uuid.uuid4()
        self.task.task_type = 'POND_QUALITY'
        self.task.date = date.today()
        self.task.status = 'TODO'
        self.task.cycle_id = self.cycle.id

        self.task2 = MagicMock(spec=Task)
        self.task2.id = uuid.uuid4()
        self.task2.task_type = 'FISH_SAMPLING'
        self.task2.date = date.today() + timedelta(days=1)
        self.task2.status = 'TODO'
        self.task2.cycle_id = self.cycle.id

        self.task3 = MagicMock(spec=Task)
        self.task3.id = uuid.uuid4()
        self.task3.task_type = 'POND_QUALITY'
        self.task3.date = date.today()
        self.task3.status = 'TODO'
        self.task3.cycle_id = uuid.uuid4()

        self.task_list = [self.task, self.task2, self.task3]

        self.expected_output = [task for task in self.task_list if task.cycle_id == self.cycle.id]

    def test_list_tasks_api(self):
        with patch('tasks.services.list_service_impl.ListServiceImpl.list_tasks') as mock_list_tasks, \
            patch('cycle.services.cycle_service.CycleService.get_active_cycle') as mock_get_active_cycle:

            mock_list_tasks.return_value = self.expected_output
            mock_get_active_cycle.return_value = self.cycle

            response = list_tasks(self.request)

            self.assertEqual(response[0].id, self.expected_output[0].id)
            self.assertEqual(response[0].task_type, self.expected_output[0].task_type)
            self.assertEqual(response[1].id, self.expected_output[1].id)
            self.assertEqual(response[1].task_type, self.expected_output[1].task_type)
    
    def test_list_tasks_api_empty(self):
        with patch('tasks.services.list_service_impl.ListServiceImpl.list_tasks') as mock_list_tasks, \
            patch('cycle.services.cycle_service.CycleService.get_active_cycle') as mock_get_active_cycle:

            mock_list_tasks.return_value = []
            mock_get_active_cycle.return_value = self.cycle

            response = list_tasks(self.request)

            self.assertEqual(response, [])

    def test_list_tasks_api_not_found_cycle(self):
        with patch('tasks.services.list_service_impl.ListServiceImpl.list_tasks') as mock_list_tasks, \
            patch('cycle.services.cycle_service.CycleService.get_active_cycle') as mock_get_active_cycle:

            mock_get_active_cycle.return_value = None
            
            with self.assertRaises(HttpError):
                response = list_tasks(self.request)
