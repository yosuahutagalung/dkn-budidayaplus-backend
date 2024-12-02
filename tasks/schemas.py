from ninja import Schema
from pydantic import UUID4, validator
from datetime import date
from typing import Optional
from typing import List

from pydantic.functional_validators import field_validator
from tasks.enums import TaskStatus, TaskPeriod


class TaskSchema(Schema):
    id: UUID4
    task_type: str
    date: date
    status: str
    cycle_id: UUID4
    assignee: Optional[str] = ''

    @staticmethod
    def resolve_task_type(obj):
        return ' '.join(obj.task_type.split('_')).title()

class SortedTaskSchema(Schema):
    past: List[TaskSchema]
    upcoming: List[TaskSchema]

class TaskStatusSchema(Schema):
    status: TaskStatus

class TaskFilterSchema(Schema):
    limit: int = 10
    offset: int = 0
    period: Optional[TaskPeriod] = None
    assignee: Optional[str] = None
