from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from dnd.model.tasks import Task
from dnd.shemas.tasks import Task as TaskShemas
from dnd.shemas.taskqwestionai import Mission
from typing import Optional
#from win32comext.shell.demos.servers.folder_view import tasks


async def create_task(
    db: AsyncSession,
    shemas: TaskShemas,
    token:dict,
    tasks_qwest:Optional[Mission | None] = None

) -> Task:
    """Создание новой задачи в БД."""
    if tasks_qwest is not None:

        db_task = Task(
            name=shemas.name,
            date_start=shemas.date_start,
            date_end=shemas.date_end,
            description=shemas.description,
            name_quest=tasks_qwest.name_quest,
            quest=tasks_qwest.quest,
            health=tasks_qwest.bonus.health,
            manna=tasks_qwest.bonus.manna,
            power=tasks_qwest.bonus.power,
            intelligence=tasks_qwest.bonus.intelligence,
            agility=tasks_qwest.bonus.agility,
            loot=tasks_qwest.bonus.loot,
            user_id=int(token.get('sub'))
        )
    else:
        db_task = Task(
            name=shemas.name,
            date_start=shemas.date_start,
            date_end=shemas.date_end,
            description=shemas.description,
            user_id=int(token.get('sub'))

        )
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task


async def get_task(db: AsyncSession, task_id: int) -> Task | None:
    """Получение задачи по ID."""
    stmt = select(Task).where(Task.id == task_id)
    result = await db.execute(stmt)
    return result.scalars().first()


async def get_tasks(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[Task]:
    """Получение списка задач с пагинацией."""
    stmt = select(Task).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_tasks_by_name(db: AsyncSession, user_id: int,name: str) -> list[Task]:
    pass


async def get_tasks_by_user(db: AsyncSession, user_id: int) -> list[Task]:
    """Получение всех задач конкретного пользователя."""
    stmt = select(Task).where(Task.user_id == user_id)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def update_task(
    db: AsyncSession,
    task_id: int,
    name: str | None = None,
    date_start: str | None = None,
    date_end: str | None = None,
    description: str | None = None,
    name_quest: str | None = None,
    quest: str | None = None,
    user_id: int | None = None
) -> Task | None:
    """Обновление задачи."""
    task = await get_task(db, task_id)
    if not task:
        return None

    if name is not None:
        task.name = name
    if date_start is not None:
        task.date_start = date_start
    if date_end is not None:
        task.date_end = date_end
    if description is not None:
        task.description = description
    if name_quest is not None:
        task.name_quest = name_quest
    if quest is not None:
        task.quest = quest
    if user_id is not None:
        task.user_id = user_id

    await db.commit()
    await db.refresh(task)
    return task


async def delete_task(db: AsyncSession, task_id: int) -> bool:
    """Удаление задачи по ID. Возвращает True при успешном удалении."""
    task = await get_task(db, task_id)
    if not task:
        return False

    await db.delete(task)
    await db.commit()
    return True



