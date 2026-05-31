from __future__ import annotations  # Позволяет использовать отложенные аннотации
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

class Taskbase(BaseModel):
    name: str = Field(description="название задачи")
    date_start: str = Field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d'))
    date_end: str
    description: str = Field(description="описание задачи")

class Task(Taskbase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description='id задачи')
    flag_ai: bool = Field(description="создана ли AI")
    subtasks: Optional[List[Task]] = Field(default_factory=list)  # Теперь работает!

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "name": "Имя задачи",
                "date_end": "2024-12-31",
                "description": "Найти и победить главного босса",
                "flag_ai": False,
                "subtasks": [
                    {
                        "name": "Найти меч",
                        "date_end": "2024-11-30",
                        "description": "Выковать легендарный меч",
                        "flag_ai": True
                    }
                ]
            }
        }


class Promttask(Taskbase):
    """Модель для отправки в AI (без id, flag_ai, subtasks)"""

    @classmethod
    def from_task(cls, task: Task) -> 'Promttask':
        """Создает Promttask из Task"""
        return cls(
            name=task.name,
            date_start=task.date_start,
            date_end=task.date_end,
            description=task.description
        )
    def to_json(self) -> str:
        """Преобразует в JSON строку для AI"""
        return self.model_dump_json(ensure_ascii=False)

class list_subtask(BaseModel):
    subtask: Optional[list[Promttask]]