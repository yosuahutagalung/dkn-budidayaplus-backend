from django.test import TestCase
from unittest.mock import patch, MagicMock
from tasks.services.set_status_service_impl import SetStatusServiceImpl
from tasks.models import Task
from tasks.repositories.set_status_repo import SetStatusRepo
import uuid

class SetStatusServiceImplTest(TestCase):

    @patch.object(SetStatusRepo, 'set_status')
    def test_set_status_success_stub(self, mock_set_status):
        task_id = uuid.uuid4()
        status = 'DONE'
        mock_set_status.return_value = MagicMock(spec=Task)

        updated_task = SetStatusServiceImpl().set_status(task_id=task_id, status=status)

        mock_set_status.assert_called_once_with(task_id=task_id, status=status)
        self.assertIsInstance(updated_task, Task)

    @patch.object(SetStatusRepo, 'set_status')
    def test_set_status_task_not_found_stub(self, mock_set_status):
        task_id = uuid.uuid4()
        status = 'TODO'
        mock_set_status.side_effect = Task.DoesNotExist

        with self.assertRaises(Task.DoesNotExist):
            SetStatusServiceImpl().set_status(task_id=task_id, status=status)

        mock_set_status.assert_called_once_with(task_id=task_id, status=status)