from abc import ABC, abstractmethod
from domain.entities.task import Task
from typing import List


class iTaskRepository(ABC):
    @abstractmethod
    async def save_task(self, task: Task):
        pass

    # @abstractmethod
    # def save_many_task(self, tasks: List[Task]):
    #     pass
    #
    # @abstractmethod
    # def req_ai_mission(self, task: Task):
    #     pass      