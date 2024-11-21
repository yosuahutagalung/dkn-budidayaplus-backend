from django.test import TestCase
from unittest.mock import patch, MagicMock
from tasks.models import Task
from tasks.repositories.set_status_repo import SetStatusRepo
import uuid

class SetStatusRepoTest(TestCase):
    def setUp(self):
        self.task_id = uuid.uuid4()
        self.mock_task = MagicMock(spec=Task)
        self.mock_task.id = self.task_id
        self.mock_task.status = 'TODO'

    @patch('tasks.models.Task.objects.get')
    def test_set_status_success(self, mock_get):
        mock_get.return_value = self.mock_task
        updated_task = SetStatusRepo.set_status(task_id=self.task_id, status='IN_PROGRESS')

        mock_get.assert_called_once_with(id=self.task_id)
        self.assertEqual(updated_task.status, 'IN_PROGRESS')
        self.mock_task.save.assert_called_once()

    @patch('tasks.models.Task.objects.get')
    def test_set_status_task_not_found(self, mock_get):
        mock_get.side_effect = Task.DoesNotExist

        with self.assertRaises(Task.DoesNotExist):
            SetStatusRepo.set_status(task_id=self.task_id, status='IN_PROGRESS')

        mock_get.assert_called_once_with(id=self.task_id)
