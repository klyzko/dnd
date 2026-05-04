from dnd.shemas.tasks import Task,Promttask
from dnd.db.task_crud import create_task,get_tasks_by_user,get_tasks
from sqlalchemy.ext.asyncio import AsyncSession
from dnd.services.task_service import dndtask
from dnd.services.task_sub_ai import subtask
from dnd.services.sheduler.sheduler_task_ai import sheduler_task_ai
from dnd.core.logger_config import logg
from api.users import login


#from shemas.tasks import Task as db_task


async def add_task(task: Task,db: AsyncSession,token:dict):
    """"
    Create mission and add task to database
    """
    answere =[]
    pomttask =Promttask.from_task(task)
    user_prompt = pomttask.to_json()
    mission = await dndtask(user_prompt)
    if mission is None:
       await sheduler_task_ai(task)
    answere.append(await create_task(db,task,token,mission))
    if not task.flag_ai:
        return answere
    promtsub = Promttask.from_task(task)
    user_subt = promtsub.to_json()
    sub = await subtask(user_subt)
    for one_sub in sub.subtask:
        logg.info(one_sub)
        one_sub_json = one_sub.to_json()
        mission_sub = await dndtask(one_sub_json)
        if mission_sub is None:
           await sheduler_task_ai(one_sub)
        answere.append(await create_task(db,one_sub,token,mission_sub))

    return answere

async def get_tasks_users(db: AsyncSession,token:dict):
    return get_tasks_by_user(db,token.get('sub'))


async def get_task_by_name(db: AsyncSession,token:dict):
    task_id=get_tasks(db,token.get('sub'))
    if task_id is None:
        return {404:"task not found"}

