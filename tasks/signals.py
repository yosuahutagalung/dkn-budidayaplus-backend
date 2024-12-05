from django.dispatch import receiver
from cycle.services.cycle_service import CycleService
from tasks.models import Task, TaskTemplate
from datetime import timedelta
from tasks.enums import TaskStatus
from cycle.signals import create_cycle_signal

@receiver(create_cycle_signal, sender=CycleService)
def create_tasks(sender, instance, created, **kwargs):
    if created:
        cycle = instance
        start_date = cycle.start_date
        pond_fish_amount_list = cycle.pond_fish_amount.all()
        task_templates = TaskTemplate.objects.all()

        for pond_fish_amt in pond_fish_amount_list:
            pond = pond_fish_amt.pond
            for template in task_templates:
                task_date = start_date + timedelta(days=template.day_of_culture - 1)
                Task.objects.create(
                    task_type=template.task_type,
                    date=task_date,
                    status=TaskStatus.TODO.value,
                    cycle=cycle,
                    assignee='',
                    pond=pond
                )


