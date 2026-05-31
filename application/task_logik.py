#rom api.v1.shemas import Task,Promttask
#from infrastructure.db.repositories.user_repositories import get_tasks_by_user,get_tasks
#from Scripts.jsonpointer import parser
from pyexpat.errors import messages
from sqlalchemy.ext.asyncio import AsyncSession
from domain.repositories.itask_repositories import iTaskRepository
from ai.ports.ILLMclient import LLMClient
from ai.ports.llm_errors import (
    LLMError,
    LLMTimeoutError,
    LLMUnavailableError,
    LLMRateLimitError,
    LLMResponseFormatError
                        )
from ai.ports.illparser import IllParser
from domain.entities.task import Task as Task_ent
from ai.domain.entities.Message import Message
from ai.mapper import Mapper
#from shemas.tasks import Task as db_task

class TaskLogik:
    def __init__(self,itaskRepository:iTaskRepository,client:LLMClient,parser_mission:IllParser,parser_sub:IllParser):
        self.repo=itaskRepository
        self.client=client
        self.parser_mission=parser_mission
        self.parser_sub=parser_sub


    async def create(self,task:Task_ent,promt_sub:str,promt_ai:str,flag_ai:bool):
        try:
            if not task.flag_execution:
                return await self.repo.save_task(task)
            all_task = task
            i = 0
            while i!=3:
                try:
                    if all_task == task:
                        message_sub = Message(promt_sub,task.get_by_subtasks())
                        sub_content = await self.client.chat(message_sub,"deepseek-chat")
                        sub_content = self.parser_sub.parse(sub_content)
                        all_task = Mapper.dict_to_task(sub_content)
                    if all_task != task:
                        sub_for_mission = Mapper.resp_qwest(sub_content)
                        message_ai = Message(promt_ai,sub_for_mission)
                        mission_ai = await self.client.chat(message_ai,"deepseek-chat")
                        mission_ai = self.parser_mission.parse(mission_ai)
                        all_task_dict = Mapper.union_list_dict(sub_content,mission_ai)
                        all_task = Mapper.dict_to_task(all_task_dict)
                    return await self.repo.save_task(all_task)
                except LLMResponseFormatError as e:
                    i= i + 1
                    if i == 3:
                        return await self.repo.save_task(all_task)
                except LLMRateLimitError as e:
                    i = i + 1
                    if i == 3:
                        return await self.repo.save_task(all_task)
                except LLMUnavailableError as e:
                    i = i + 1
                    if i == 3:
                        return await self.repo.save_task(all_task)
                except LLMTimeoutError as e:
                    i = i + 1
                    if i == 3:
                        return await self.repo.save_task(all_task)
                except LLMError as e:
                    i = i + 1
                    if i == 3:
                        return await self.repo.save_task(all_task)
        except Exception as e:
            raise e

    async def get_task(self):
        pass


    async def update_task(self,task:Task_ent):
        pass


    async def delete_task(self,task:Task_ent):
        pass







# async def add_task(task: Task,db: AsyncSession,token:dict):
#     """"
#     Create mission and add task to database
#     """
#     answere =[]
#     pomttask =Promttask.from_task(task)
#     user_prompt = pomttask.to_json()
#     mission = await dndtask(user_prompt)
#     if mission is None:
#        await sheduler_task_ai(task)
#     answere.append(await create _task(db,task,token,mission))
#     if not task.flag_ai:
#         return answere
#     promtsub = Promttask.from_task(task)
#     user_subt = promtsub.to_json()
#     sub = await subtask(user_subt)
#     for one_sub in sub.subtask:
#         logg.info(one_sub)
#         one_sub_json = one_sub.to_json()
#         mission_sub = await dndtask(one_sub_json)
#         if mission_sub is None:
#            await sheduler_task_ai(one_sub)
#         answere.append(await create_task(db,one_sub,token,mission_sub))
#
#     return answere

# async def get_tasks_users(db: AsyncSession,token:dict):
#     return get_tasks_by_user(db,token.get('sub'))
#
#
# async def get_task_by_name(db: AsyncSession,token:dict):
#     task_id=get_tasks(db,token.get('sub'))
#     if task_id is None:
#         return {404:"task not found"}

