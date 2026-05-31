from api.v1.shemas.users import UserCreate
from fastapi import Depends, APIRouter
from infrastructure.db.repositories.user_repositories import create_user
from sqlalchemy.ext.asyncio import AsyncSession
from dependency.depend import get_db
router = APIRouter()


@router.post("/auth/register")
async def registration( user: UserCreate, db: AsyncSession = Depends(get_db)):
    await create_user(db,user.email,user.username,user.password)
