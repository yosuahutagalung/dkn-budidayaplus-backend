from django.test import TestCase
from unittest.mock import patch, MagicMock
from tasks.services.set_status_service_impl import SetStatusServiceImpl
from tasks.models import Task
import uuid

class SetStatusServiceImplTest(TestCase):

    def test_set_status_success(self):
        with patch('tasks.repositories.set_status_repo.SetStatusRepo.set_status') as mock_set_status:
            task_id = uuid.uuid4()
            status = "TODO"

            mock_task = MagicMock(spec=Task)
            mock_task.id = task_id
            mock_task.status = status

            mock_set_status.return_value = mock_task

            updated_task = SetStatusServiceImpl.set_status(task_id=task_id, status=status)

            mock_set_status.assert_called_once_with(task_id=task_id, status=status)
            self.assertEqual(updated_task.id, task_id)
            self.assertEqual(updated_task.status, status)

    def test_set_status_failure(self):
        with patch('tasks.repositories.set_status_repo.SetStatusRepo.set_status') as mock_set_status:
            task_id = uuid.uuid4()
            status = "DONE"

            mock_set_status.side_effect = Task.DoesNotExist

            with self.assertRaises(Task.DoesNotExist):
                SetStatusServiceImpl.set_status(task_id=task_id, status=status)

            mock_set_status.assert_called_once_with(task_id=task_id, status=status)
