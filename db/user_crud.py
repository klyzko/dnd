from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from dnd.model.users import User
from dnd.model.hero import Hero
from dnd.model.roles import Role
from  shemas.users import UserCreate


async def create_user(db: AsyncSession ,user_schema: UserCreate ):
    db_user = User(name=user_schema.username,email=user_schema.email, password=user_schema.hashed_password)
    db_user.hero =Hero(name=user_schema.hero_name,power=0,health=0,manna=0,intelligence=0,agility=0)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user_rolepermissions(db: AsyncSession , id: int):

        stmt = select(User).where(User.id == id).options(
            selectinload(User.roles).selectinload(Role.permissions)
        )
        result = await db.execute(stmt)
        user = result.scalars().first()
        return user


async def get_user_by_email(db: AsyncSession, email: str, password: str):
    stmt = select(User).where(User.email == email).options()
    result = await db.execute(stmt)
    user = result.scalars().first()
    return user