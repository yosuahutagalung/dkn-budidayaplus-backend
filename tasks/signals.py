from django.db.models.signals import post_save
from django.dispatch import receiver
from tasks.models import Task, TaskTemplate
from cycle.models import Cycle
from datetime import timedelta
from tasks.enums import TaskStatus

@receiver(post_save, sender=Cycle)
def create_tasks(sender, instance, created, **kwargs):
    if created:
        counter = 0

        cycle = instance
        start_date = cycle.start_date

        task_templates = TaskTemplate.objects.all()

        for template in task_templates:
            counter += 1
            task_date = start_date + timedelta(days=template.day_of_culture - 1)
            Task.objects.create(
                task_type=template.task_type,
                date=task_date,
                status=TaskStatus.TODO,
                cycle=cycle,
                assignee='',
            )

        print(f'Successfully copied {counter} TaskTemplate entries to Task for Cycle {cycle.id}')
