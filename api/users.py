from fastapi import APIRouter,Depends,status,Response,HTTPException
from dnd.shemas.users import UserReqwest,UserCreate
from dnd.db.depend import get_db
from sqlalchemy.ext.asyncio import async_sessionmaker
from dnd.db.user_crud import create_user,get_user_by_email
from dnd.dependencies.jwt import token as jwts
from fastapi.params import Query
from dnd.db.depend_redis import get_redis
import redis.asyncio as redis




router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/register")
async def register_user(
        user: UserCreate,
        response: Response,
        db: async_sessionmaker = Depends(get_db),
        client_type: str = Query("web", description="web или mobile")  # Определяем тип клиента
):
    db_user =await create_user(db, user)
    if not db_user:
        raise HTTPException(status_code=400, detail="User creation failed")

    try:
        access_token = await jwts.create_access_token(db_user.id)
        refresh_token = await jwts.create_refresh_token(db_user.id)

        # Для веба - устанавливаем куки
        if client_type == "web":
            await jwts.set_cookie(response, access_token, 'access_token')
            await jwts.set_cookie(response, refresh_token, 'refresh_token')
            return status.HTTP_201_CREATED

        # Для мобилки - возвращаем токены в теле ответа
        elif client_type == "mobile":
            return {
                "status": "success",
                "message": "User registered successfully",
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer"
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Token creation failed: {str(e)}")




@router.post("/login")
async def login(user: UserReqwest,
                response: Response,
                db: async_sessionmaker = Depends(get_db),
                client_type: str = Query("web", description="web или mobile")
                ):
    try:
        db_user = await get_user_by_email(db, user.email)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        if not db_user.verify_password(user.password,db_user.password):
            raise HTTPException(status_code=404, detail="Incorrect password")
        access_token = await jwts.create_access_token(db_user.id)
        refresh_token = await jwts.create_refresh_token(db_user.id)

        # Для веба - устанавливаем куки
        if client_type == "web":
            await jwts.set_cookie(response, access_token, 'access_token')
            await jwts.set_cookie(response, refresh_token, 'refresh_token')
            return status.HTTP_201_CREATED

        # Для мобилки - возвращаем токены в теле ответа
        elif client_type == "mobile":
            return {
                "status": "success",
                "message": "User registered successfully",
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer"
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Token creation failed: {str(e)}")


@router.post("/logout")
async def logout(
        response: Response,
        client_type: str = Query("web", description="web или mobile"),
        token: str = Depends(jwts.get_token()),
        token_refresh = Depends(jwts.get_token(jwts.typs_token.refresh_token)),
        red: redis.Redis = Depends(get_redis),

):
    token_verified = await jwts.verify_token(token)
    if token_verified is not None:
        jti = token_verified.get('jti')
        await  jwts.get_blacklist_token(jti,red)

    token_verified_refresh = await jwts.verify_token(token_refresh)
    if token_verified_refresh is not None:
        jti_ref = token_verified_refresh.get('jti')
        await  jwts.get_blacklist_token(jti_ref,red)

    if client_type == "web":
        # Просто удаляем куки на клиенте
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return {"message": "Successfully logged out"}

    # Для мобилки - просто говорим клиенту удалить токены
    return {"message": "Please delete stored tokens on client side"}


