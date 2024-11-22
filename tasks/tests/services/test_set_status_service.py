from django.test import TestCase
from unittest.mock import patch, MagicMock
from tasks.services.set_status_service_impl import SetStatusServiceImpl
from tasks.models import Task
from tasks.repositories.set_status_repo import SetStatusRepo
import uuid

class SetStatusServiceImplTest(TestCase):

    # use stubs to test the service layer
    @patch('tasks.repositories.set_status_repo.SetStatusRepo.set_status')
    def test_set_status(self, mock_set_status):
        class StubTask:
            def __init__(self, id):
                self.id = id
                self.status = 'TODO'

        task_id = uuid.uuid4()
        status = 'TODO'

        mock_set_status.return_value = StubTask(task_id)

        updated_task = SetStatusServiceImpl.set_status(task_id=task_id, status=status)

        mock_set_status.assert_called_once_with(task_id=task_id, status=status)

        self.assertEqual(updated_task.id, task_id)
        self.assertEqual(updated_task.status, status)

    @patch('tasks.repositories.set_status_repo.SetStatusRepo.set_status')
    def test_set_status_task_not_found(self, mock_set_status):
        task_id = uuid.uuid4()
        status = 'TODO'

        mock_set_status.side_effect = Task.DoesNotExist

        with self.assertRaises(Task.DoesNotExist):
            SetStatusServiceImpl.set_status(task_id=task_id, status=status)

        mock_set_status.assert_called_once_with(task_id=task_id, status=status)