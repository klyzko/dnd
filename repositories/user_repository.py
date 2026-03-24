from dnd.models.users import UserCreate
from fastapi import Depends, APIRouter, HTTPException
from dnd.db.user_crud import create_user

router = APIRouter()


router.post("/auth/register")
async def registration(user: UserCreate):
    create_user(user.username, user.email, user.password)

