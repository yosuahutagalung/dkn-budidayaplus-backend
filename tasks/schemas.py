from ninja import Schema
from pydantic import UUID4
from datetime import date
from typing import Optional
from typing import List

class TaskSchema(Schema):
    id: UUID4
    task_type: str
    date: date
    status: str
    cycle_id: UUID4
    assignee: Optional[str] = ''

class SortedTaskSchema(Schema):
    past: List[TaskSchema]
    upcoming: List[TaskSchema]