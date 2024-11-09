# Generated by Django 5.1.1 on 2024-11-09 18:25

import django.db.models.deletion
import tasks.enums
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cycle', '0002_remove_cycle_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskTemplate',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('task_type', models.CharField(choices=tasks.enums.TaskType.choices, max_length=20)),
                ('day_of_culture', models.PositiveIntegerField()),
            ],
            options={
                'ordering': ['day_of_culture'],
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('task_type', models.CharField(choices=tasks.enums.TaskType.choices, max_length=20)),
                ('date', models.DateField()),
                ('status', models.CharField(choices=tasks.enums.TaskStatus.choices, default=tasks.enums.TaskStatus['TODO'], max_length=4)),
                ('assignee', models.CharField(max_length=13)),
                ('cycle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cycle.cycle')),
            ],
            options={
                'ordering': ['date'],
            },
        ),
    ]