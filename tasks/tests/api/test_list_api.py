from unittest.mock import patch, MagicMock
from django.test import TestCase
from tasks.models import Task
from datetime import date, timedelta
from cycle.models import Cycle
from django.http import HttpRequest
from django.contrib.auth.models import User
from tasks.api import list_tasks, list_tasks_sorted, assign_task
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
        self.task.assignee = "test_assignee"

        self.task2 = MagicMock(spec=Task)
        self.task2.id = uuid.uuid4()
        self.task2.task_type = 'FISH_SAMPLING'
        self.task2.date = date.today() + timedelta(days=1)
        self.task2.status = 'TODO'
        self.task2.cycle_id = self.cycle.id

        self.task3 = MagicMock(spec=Task)
        self.task3.id = uuid.uuid4()
        self.task3.task_type = 'FOOD_SAMPLING'
        self.task3.date = date.today() - timedelta(days=1)
        self.task3.status = 'TODO'
        self.task3.cycle_id = self.cycle.id

        self.task4 = MagicMock(spec=Task)
        self.task4.id = uuid.uuid4()
        self.task4.task_type = 'POND_QUALITY'
        self.task4.date = date.today()
        self.task4.status = 'TODO'
        self.task4.cycle_id = uuid.uuid4()

        self.task_list = [self.task, self.task2, self.task3, self.task4]

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
            self.assertEqual(response[2].id, self.expected_output[2].id)
            self.assertEqual(response[2].task_type, self.expected_output[2].task_type)
            self.assertEqual(len(response), 3)
            self.assertNotIn(self.task4, response)
    

    def test_list_tasks_api_empty(self):
        with patch('tasks.services.list_service_impl.ListServiceImpl.list_tasks') as mock_list_tasks, \
            patch('cycle.services.cycle_service.CycleService.get_active_cycle') as mock_get_active_cycle:

            mock_list_tasks.return_value = []
            mock_get_active_cycle.return_value = self.cycle

            response = list_tasks(self.request)

            self.assertEqual(response, [])


    def test_list_tasks_api_not_found_cycle(self):
        with patch('cycle.services.cycle_service.CycleService.get_active_cycle') as mock_get_active_cycle:

            mock_get_active_cycle.return_value = None
            
            with self.assertRaises(HttpError):
                list_tasks(self.request)

            
    def test_list_tasks_api_sorted(self):
        with patch('tasks.services.list_service_impl.ListServiceImpl.list_tasks_sorted_date') as mock_list_tasks_sorted_date, \
            patch('cycle.services.cycle_service.CycleService.get_active_cycle') as mock_get_active_cycle:

            mock_list_tasks_sorted_date.return_value = {
                "upcoming": [task for task in self.task_list if task.date >= date.today()],
                "past": [task for task in self.task_list if task.date < date.today()]
            }
            mock_get_active_cycle.return_value = self.cycle

            response = list_tasks_sorted(self.request)

            self.assertEqual(response["upcoming"][0].id, self.task.id)
            self.assertEqual(response["upcoming"][1].id, self.task2.id)
            self.assertEqual(response["past"][0].id, self.task3.id)
        

    def test_lists_tasks_api_sorted_no_cycle(self):
        with patch('cycle.services.cycle_service.CycleService.get_active_cycle') as mock_get_active_cycle:

            mock_get_active_cycle.return_value = None
            
            with self.assertRaises(HttpError):
                list_tasks_sorted(self.request)
    
    def test_assign_task_success(self):
        with patch('tasks.services.list_service_impl.ListServiceImpl.assign_task') as mock_assign_task:
            mock_assign_task.return_value = self.task
            self.task.assignee = self.task.assignee 

            response = assign_task(self.request, str(self.task.id), self.task.assignee)

            self.assertEqual(response.id, self.task.id)
            self.assertEqual(response.assignee, self.task.assignee)
            mock_assign_task.assert_called_once_with(task_id=str(self.task.id), assignee=self.task.assignee)
    
    def test_assign_task_not_found(self):
        with patch('tasks.services.list_service_impl.ListServiceImpl.assign_task') as mock_assign_task:
            mock_assign_task.side_effect = HttpError(404, "Task not found")

            with self.assertRaises(HttpError) as context:
                assign_task(self.request, str(uuid.uuid4()), self.task.assignee)

            self.assertEqual(context.exception.status_code, 404)
            self.assertEqual(str(context.exception), "Task not found")
            mock_assign_task.assert_called_once()
