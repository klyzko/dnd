
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from dnd.model.users import User
from dnd.model.hero import Hero
from dnd.model.roles import Role
from dnd.shemas.users import UserCreate
from dnd.core.logger_config import logg


async def create_user(db: AsyncSession ,user_schema: UserCreate ):
    db_user = User(name=user_schema.username,email=user_schema.email)
    db_user.set_password(user_schema.password)
    logg.info(db_user.password)
    db_user.hero =Hero(name=user_schema.hero_name,power=0,health=0,manna=0,intelligence=0,agility=0)
    stmt = select(Role).where(Role.id == 1).options()
    result = await db.execute(stmt)
    role = result.scalars().first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    db_user.roles.append(role)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user_rolepermissions(db: AsyncSession , id: int):

        stmt = select(User).where(User.id == id).options(
            selectinload(User.roles).selectinload(Role.permision)
        )
        result = await db.execute(stmt)
        user = result.scalars().first()
        return user


async def get_user_by_email(db: AsyncSession, email: str):
    stmt = select(User).where(User.email == email).options()
    result = await db.execute(stmt)
    user = result.scalars().first()
    return user