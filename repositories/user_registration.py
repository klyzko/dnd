from dnd.shemas.users import UserCreate
from fastapi import Depends, APIRouter, HTTPException
from dnd.db.user_crud import create_user
from sqlalchemy.ext.asyncio import AsyncSession
from dnd.db.depend import get_db
router = APIRouter()


@router.post("/auth/register")
async def registration( user: UserCreate, db: AsyncSession = Depends(get_db)):
    await create_user(db,user.username, user.email, user.password)

