from abc import ABC, abstractmethod
from domain.entities.task import Task

class Iai(ABC):
    @abstractmethod
    async def qwesttask(self,task:Task):
        pass

    @abstractmethod
    async def subtask(self,task:Task):
        pass