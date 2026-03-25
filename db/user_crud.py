from fastapi.params import Depends
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from dnd.model.users import User
from dnd.model.hero import Hero


async def create_user(db: AsyncSession , email: str, username: str, hashed_password: str):
    db_user = User(name=username,email=email, password=hashed_password)
    db_user.hero =Hero(name=username,power="Null")
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user