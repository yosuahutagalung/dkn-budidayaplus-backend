from unittest.mock import patch, MagicMock
from django.test import TestCase
from tasks.models import Task
from tasks.api import set_status
from tasks.schemas import TaskStatusSchema
from ninja.errors import HttpError
from django.http import HttpRequest
from django.contrib.auth.models import User
import uuid

class SetStatusAPITest(TestCase):
    def setUp(self):
        self.request = MagicMock(spec=HttpRequest)
        self.request.auth = MagicMock(spec=User)

        self.task_id = uuid.uuid4()
        self.payload = TaskStatusSchema(status="DONE")

        self.mock_task = MagicMock(spec=Task)
        self.mock_task.id = self.task_id
        self.mock_task.status = self.payload.status

    def test_set_status_api_success(self):
        with patch('tasks.services.set_status_service_impl.SetStatusServiceImpl.set_status') as mock_set_status:
            mock_set_status.return_value = self.mock_task

            response = set_status(self.request, task_id=str(self.task_id), payload=self.payload)

            mock_set_status.assert_called_once_with(task_id=str(self.task_id), status=self.payload.status)
            self.assertEqual(response.id, self.mock_task.id)
            self.assertEqual(response.status, self.payload.status)

    def test_set_status_api_invalid_task(self):
        with patch('tasks.services.set_status_service_impl.SetStatusServiceImpl.set_status') as mock_set_status:
            mock_set_status.side_effect = Task.DoesNotExist

            with self.assertRaises(HttpError):
                set_status(self.request, task_id=str(self.task_id), payload=self.payload)

            mock_set_status.assert_called_once_with(task_id=str(self.task_id), status=self.payload.status)


    def test_set_status_api_invalid_status(self):
        invalid_status = "INVALID_STATUS"

        with self.assertRaises(ValueError) as context:
            TaskStatusSchema(status=invalid_status)

        self.assertIn("Input should be 'TODO' or 'DONE'", str(context.exception))