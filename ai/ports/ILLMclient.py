from abc import ABC, abstractmethod
from ai.domain.entities.Message import Message

class LLMClient(ABC):
    @abstractmethod
    async def chat(self,message: Message,model:str,**kwargs):
        pass


    @abstractmethod
    async def parsresponse(self,content:str):
        pass


    @abstractmethod
    async def image(self,message: Message,model:str,**kwargs):
        pass