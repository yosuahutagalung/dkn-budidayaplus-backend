from django.contrib.auth.models import User
from django.test import TestCase
from django.test import TestCase
from unittest.mock import patch, MagicMock

from ninja.errors import HttpError
from cycle.models import Cycle
from tasks.api import filter_tasks
from tasks.enums import TaskPeriod
from tasks.models import Task
from django.utils import timezone
from datetime import timedelta
from django.http import HttpRequest
import uuid

from tasks.schemas import TaskFilterSchema

class TestTaskFilterAPI(TestCase):
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

        self.cycle = MagicMock(spec=Cycle)
        self.cycle.id = uuid.uuid4()

        self.task_repository = [self.task1, self.task2, self.task3, self.task4]

    def test_filter_tasks_api(self):
        with patch('tasks.services.filter_service_impl.FilterServiceImpl.filter_tasks') as mock_filter, \
            patch('cycle.services.cycle_service.CycleService.get_active_cycle') as mock_cycle:

            filters = TaskFilterSchema(period=None, assignee="Rafi")
            filtered_tasks = [task for task in self.task_repository if task.assignee == filters.assignee]

            mock_cycle.return_value = self.cycle
            mock_filter.return_value = filtered_tasks
            mock_request = MagicMock(spec=HttpRequest)
            mock_request.auth = MagicMock(spec=User)

            expected_response = filtered_tasks[filters.offset : filters.offset + filters.limit]

            response = filter_tasks(mock_request, filters)
            self.assertEqual(response, expected_response)


    def test_filter_tasks_api_with_period(self):
        with patch('tasks.services.filter_service_impl.FilterServiceImpl.filter_tasks') as mock_filter, \
            patch('cycle.services.cycle_service.CycleService.get_active_cycle') as mock_cycle:

            filters = TaskFilterSchema(period=TaskPeriod.UPCOMING, assignee="Rafi")
            filtered_tasks = [task for task in self.task_repository if task.assignee == filters.assignee]

            mock_cycle.return_value = self.cycle
            mock_filter.return_value = filtered_tasks
            mock_request = MagicMock(spec=HttpRequest)
            mock_request.auth = MagicMock(spec=User)

            expected_response = filtered_tasks[filters.offset : filters.offset + filters.limit]

            response = filter_tasks(mock_request, filters)
            self.assertEqual(response, expected_response)


    def test_filter_tasks_cycle_not_found(self):
        with patch('tasks.services.filter_service_impl.FilterServiceImpl.filter_tasks') as mock_filter, \
            patch('cycle.services.cycle_service.CycleService.get_active_cycle') as mock_cycle:

            filters = TaskFilterSchema(period=TaskPeriod.UPCOMING, assignee="Rafi")
            filtered_tasks = [task for task in self.task_repository if task.assignee == filters.assignee]

            mock_cycle.return_value = None
            mock_filter.return_value = filtered_tasks
            mock_request = MagicMock(spec=HttpRequest)
            mock_request.auth = MagicMock(spec=User)

            with self.assertRaises(HttpError) as context:
                filter_tasks(mock_request, filters)
                self.assertEqual(context.exception.message, "Data tidak ditemukan")
    
    def test_filter_tasks_by_date_success(self):
        with patch('tasks.services.filter_service_impl.FilterServiceImpl.filter_tasks_by_date') as mock_filter, \
             patch('cycle.services.cycle_service.CycleService.get_active_cycle') as mock_cycle:

            mock_cycle.return_value = self.cycle
            filter_date = timezone.now().date() 

            mock_filter.return_value = [task for task in self.task_repository if task.date == filter_date]

            mock_request = MagicMock(spec=HttpRequest)
            mock_request.auth = MagicMock()

            response = filter_tasks_by_date(mock_request, date=filter_date)
            
            self.assertEqual(response, mock_filter.return_value)
    
    def test_filter_tasks_by_date_no_tasks_found(self):
        with patch('tasks.services.filter_service_impl.FilterServiceImpl.filter_tasks_by_date') as mock_filter, \
             patch('cycle.services.cycle_service.CycleService.get_active_cycle') as mock_cycle:

            mock_cycle.return_value = self.cycle
            
            filter_date = timezone.now().date() + timedelta(days=7)  
            mock_filter.return_value = [] 

            mock_request = MagicMock(spec=HttpRequest)
            mock_request.auth = MagicMock()

            with self.assertRaises(HttpError) as context:
                filter_tasks_by_date(mock_request, date=filter_date)

            self.assertEqual(context.exception.message, "Data tidak ditemukan")
