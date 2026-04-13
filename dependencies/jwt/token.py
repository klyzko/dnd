import uuid
from jose import JWTError, jwt
from dnd.db.depend import get_db
from dnd.shemas.token import AccessTokenPayload
#from urllib3 import request

#from model.users import User
from datetime import datetime,timedelta,timezone
from dnd.db.user_crud import get_user_rolepermissions
from dnd.core.config import settings
from fastapi import HTTPException,Depends,Request,Response,Header
from typing import Optional
from dnd.core.setting import oauth2_scheme
import redis.asyncio as redis
import time
import enum
#from db.depend_redis import get_redis


class typs_token(enum.Enum):
    access_token = 'access_token'
    refresh_token = 'refresh_token'

def create_jti() -> str:
    """Генерация уникального идентификатора токена"""
    return str(uuid.uuid4())


async def create_access_token(id):
    """
    Создание JWT токена со всеми стандартными полями

    """

    async for db in get_db():  # ← используем async for для асинхронного генератора
        try:
            user = await get_user_rolepermissions(db, id)
            break  # выходим после получения сессии
        except Exception as e:
            print(f"Ошибка при получении пользователя: {e}")
            raise
        finally:
            # Сессия автоматически закроется в get_db() через finally
            pass
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    now = datetime.now(timezone.utc)
    ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
    expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    jti = create_jti()
    resurs=[]
    for roles in user.roles:
        for perm in roles.permissions:
            resurs.append(perm.resource)
    # Стандартные поля payload
    payload = AccessTokenPayload(
        iss="to-dodnd",  # Издатель токена
        sub=user.user_id,  # Собственник токена (UUID пользователя)
        aud=resurs,  # Целевые серверы
        exp=expire,  # Время истечения
        nbf=now,  # Время начала действия
        iat=now,  # Время создания
        jti=jti,  # Уникальный ID токена
        roles=user.roles,  # Кастомные данные
    )

    # Создаем JWT токен
    token_data = payload.dict()
    # Конвертируем datetime в timestamp для JWT
    for key in ['exp', 'nbf', 'iat']:
        token_data[key] = int(token_data[key].timestamp())
    SECRET_KEY = settings.secret_key
    ALGORITHM = settings.algorithm
    access_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    return access_token


async def create_refresh_token(id):
    """
    Создание JWT токена со всеми стандартными полями

    """
    async for db in get_db():  # ← используем async for для асинхронного генератора
        try:
            user = await get_user_rolepermissions(db, id)
            break  # выходим после получения сессии
        except Exception as e:
            print(f"Ошибка при получении пользователя: {e}")
            raise
        finally:
            # Сессия автоматически закроется в get_db() через finally
            pass
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    now = datetime.now(timezone.utc)
    REFRESH_TOKEN_EXPIRE_MINUTES = settings.refresh_token_expire_days
    expire = now + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    jti = create_jti()
    # Стандартные поля payload
    payload = AccessTokenPayload(
        iss="to-dodnd",  # Издатель токена
        sub=user.user_id,  # Собственник токена (UUID пользователя)
        exp=expire,  # Время истечения
        nbf=now,  # Время начала действия
        iat=now,  # Время создания
        jti=jti,  # Уникальный ID токена
    )

    # Создаем JWT токен
    token_data = payload.dict()
    # Конвертируем datetime в timestamp для JWT
    for key in ['exp', 'nbf', 'iat']:
        token_data[key] = int(token_data[key].timestamp())
    SECRET_KEY = settings.secret_key
    ALGORITHM = settings.algorithm
    access_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return access_token

#установка в черный список
async def set_blacklist_token(red: redis.Redis , token:str):
    try:
        ver_token = await verify_token(token)
        if ver_token:
            key = ver_token.get('jti')
            ttl = ver_token.get('exp') - int(time.time())
            await red.set(key, "blacklisted",ex=ttl)
    except Exception as e:
        print("The token's time is up")


async def get_blacklist_token(jti,red: redis.Redis ):
    return await red.get(jti) is not None


async def verify_token(token:str):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        if payload['exp'] < datetime.now(timezone.utc).timestamp():
            return None
        return payload
    except JWTError:

        return None


#async def get_token_from_header(
       # token: Optional[str] = Depends(oauth2_scheme)
#) -> Optional[str]:
   # """Получить токен из Authorization header"""
   # return token


#async def get_access_token_from_cookie(
        #request: Request
#) -> Optional[str]:
   # """Получить токен из куки"""
    ##token = request.cookies.get("access_token")
    #if token and token.startswith("Bearer "):
        #oken = token[7:]
    #return token

#async def get_token_from_cookie(request: Request, typs: typs_token) -> Optional[str]:
    #token = request.cookies.get(typs.value)
    #if token and token.startswith("Bearer "):
        #token = token[7:]
    #return token


# Зависимость 2: Универсальное получение токена
def get_token(token_type: typs_token = typs_token.access_token):
    """Синхронная фабрика зависимостей - оптимально для FastAPI"""

    def _get_token(
            request: Request,
            authorization: Optional[str] = Header(None)
    ) -> Optional[str]:
        # Header
        if authorization and authorization.startswith("Bearer "):
            return authorization[7:]

        # Cookie
        cookie_token = request.cookies.get(token_type.value)
        if cookie_token and cookie_token.startswith("Bearer "):
            return cookie_token[7:]

        return None

    return _get_token


async def set_cookie(response: Response, token: str, typs: typs_token):
    response.set_cookie(
        key=typs.value,
        value=f"Bearer {token}",
        httponly=True,
        max_age=settings.get_time_token(typs.value),  # 1800 секунд = 30 минут
        samesite="lax",
        secure=True
    )
