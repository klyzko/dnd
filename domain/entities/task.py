from dataclasses import dataclass
from typing import Optional

@dataclass
class Task:
    id: Optional[int] = None
    name: Optional[str] = None
    date_start: Optional[str] = None
    date_end: Optional[str] = None
    description: Optional[str] = None
    name_quest: Optional[str] = None
    quest: Optional[str] = None
    flag_execution: Optional[bool] = None
    health: Optional[int] = None
    manna: Optional[int] = None
    power: Optional[int] = None
    intelligence: Optional[int] = None
    agility: Optional[int] = None
    loot: Optional[str] = None
    user_id: Optional[int] = None
    def get_by_subtasks(self):
        return f"[{self.name},{self.date_start},{self.date_end},{self.description}]"
