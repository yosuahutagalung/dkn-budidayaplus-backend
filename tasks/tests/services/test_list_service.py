from django.test import TestCase
from unittest.mock import patch, MagicMock
from tasks.services.list_service_impl import ListServiceImpl
from tasks.models import Task
import uuid
from ninja.errors import HttpError
from django.http import HttpRequest

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
    
    def test_assign_task(self):
        with patch('tasks.repositories.list_repo.ListRepo.assign_task') as mock_assign_task:
            task_id = str(uuid.uuid4())
            assignee = "test_user"

            mock_task = MagicMock(spec=Task)
            mock_task.id = task_id
            mock_task.assignee = assignee

            mock_assign_task.return_value = mock_task
            request = MagicMock(HttpRequest)

            assigned_task = ListServiceImpl.assign_task(request=request, task_id=task_id)

            self.assertEqual(assigned_task.id, task_id)
            self.assertEqual(assigned_task.assignee, assignee)
            mock_assign_task.assert_called_once_with(request=request, task_id=task_id)

    def test_assign_task_not_found(self):
        with patch('tasks.repositories.list_repo.ListRepo.assign_task') as mock_assign_task:
            task_id = str(uuid.uuid4())
            assignee = "test_user"

            mock_assign_task.side_effect = HttpError(404, "Task not found")

            request = MagicMock(HttpRequest)
            request.auth = MagicMock()  
            request.auth.first_name = assignee  

            with self.assertRaises(HttpError) as context:
                ListServiceImpl.assign_task(request=request, task_id=task_id)

            self.assertEqual(context.exception.status_code, 404)
            self.assertEqual(str(context.exception), "Task not found")
            mock_assign_task.assert_called_once_with(request=request, task_id=task_id)