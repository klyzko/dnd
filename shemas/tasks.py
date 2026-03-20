from __future__ import annotations  # Позволяет использовать отложенные аннотации
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid


class Task(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description='id задачи')
    name: str = Field(description="название задачи")
    date_start: str = Field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d'))
    date_end: str
    description: str = Field(description="описание задачи")
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