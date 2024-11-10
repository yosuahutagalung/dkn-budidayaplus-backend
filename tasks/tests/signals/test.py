from unittest.mock import patch, MagicMock
from django.test import TestCase
from tasks.models import Task, TaskTemplate
from cycle.models import Cycle
from datetime import timedelta, date
from tasks.signals import create_tasks
from tasks.enums import TaskStatus

class TestCycleSignal(TestCase):
    @patch('tasks.models.TaskTemplate.objects.all')
    @patch('tasks.models.Task.objects.create')
    def test_create_tasks_signal(self, mock_create_task, mock_get_all_task_templates):
        start_date, end_date = date.today(), date.today() + timedelta(days=60)

        task_template_1 = MagicMock(spec=TaskTemplate)
        task_template_1.day_of_culture = 1
        task_template_1.task_type = 'POND_QUALITY'
        task_template_2 = MagicMock(spec=TaskTemplate)
        task_template_2.day_of_culture = 2
        task_template_2.task_type = 'FISH_SAMPLING'
        mock_get_all_task_templates.return_value = [task_template_1, task_template_2]

        mock_cycle = MagicMock(spec=Cycle)
        mock_cycle.start_date = start_date
        mock_cycle.end_date = end_date

        create_tasks(sender=Cycle, instance=mock_cycle, created=True)

        self.assertEqual(mock_create_task.call_count, 2)
        
        mock_create_task.assert_any_call(
            task_type='POND_QUALITY',
            date=start_date,
            status=TaskStatus.TODO,
            cycle=mock_cycle,
            assignee=''
        )
        mock_create_task.assert_any_call(
            task_type='FISH_SAMPLING',
            date=start_date + timedelta(days=1),
            status=TaskStatus.TODO,
            cycle=mock_cycle,
            assignee=''
        )
