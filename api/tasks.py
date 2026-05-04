from fastapi import APIRouter, Depends, status, Response, HTTPException
#from fontTools.misc.cython import returns
from sqlalchemy.ext.asyncio import AsyncSession
from dnd.db.depend import get_db
#from dnd.dependencies.jwt.token_refresh import token_refresh
from dnd.dependencies.jwt.token_refresh import refresh_verifide_token
from dnd.shemas.tasks import Task
#from model.tasks import Task as TaskModel
from dnd.db.task_crud import (
    create_task,
    get_task,
    get_tasks,
    get_tasks_by_user,
    update_task,
    delete_task
)
from pydantic import BaseModel
from typing import Optional



from dnd.bissneslogik.task_logik import (
    add_task

)


router = APIRouter(
    prefix=f"/tasks",
    tags=["tasks"]
)





@router.post("/create",  status_code=status.HTTP_201_CREATED)
async def create_task_route(
    task: Task,
    db: AsyncSession = Depends(get_db),
    token: dict = Depends(refresh_verifide_token)
):
    """Создание новой задачи."""
    res = await add_task(task,db,token)
    return res



@router.get("/list", response_model=list[Task])
async def get_tasks_list(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    token: dict = Depends(refresh_verifide_token)
):
    """Получение списка всех задач."""
    tasks = await get_tasks(db, skip=skip, limit=limit)
    return [
        Task(
            id=str(task.id),
            name=task.name,
            date_start=task.date_start,
            date_end=task.date_end,
            description=task.description,
            flag_ai=False,
            subtasks=[]
        )
        for task in tasks
    ]


@router.get("/my", response_model=list[Task])
async def get_my_tasks(
    db: AsyncSession = Depends(get_db),
    token: dict = Depends(refresh_verifide_token)
):
    """Получение списка задач текущего пользователя."""
    user_id = int(token.get("sub"))
    tasks = await get_tasks_by_user(db, user_id=user_id)
    return [
        Task(
            id=str(task.id),
            name=task.name,
            date_start=task.date_start,
            date_end=task.date_end,
            description=task.description,
            flag_ai=False,
            subtasks=[]
        )
        for task in tasks
    ]


@router.get("/{task_id}", response_model=Task)
async def get_task_route(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    token: dict = Depends(refresh_verifide_token)
):
    """Получение задачи по ID."""
    task = await get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return Task(
        id=str(task.id),
        name=task.name,
        date_start=task.date_start,
        date_end=task.date_end,
        description=task.description,
        flag_ai=False,
        subtasks=[]
    )


@router.put("/{task_id}", response_model=Task)
async def update_task_route(
    task_id: int,
    task_update: Task,
    db: AsyncSession = Depends(get_db),
    token: dict = Depends(refresh_verifide_token)
):
    """Редактирование задачи."""
    updated_task = await update_task(
        db=db,
        task_id=task_id,
        name=task_update.name,
        date_start=task_update.date_start,
        date_end=task_update.date_end,
        description=task_update.description,
        name_quest=task_update.name_quest,
        quest=task_update.quest
    )

    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")

    return Task(
        id=str(updated_task.id),
        name=updated_task.name,
        date_start=updated_task.date_start,
        date_end=updated_task.date_end,
        description=updated_task.description,
        flag_ai=False,
        subtasks=[]
    )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_route(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    token: dict = Depends(refresh_verifide_token)
):
    """Удаление задачи."""
    success = await delete_task(db, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return None
