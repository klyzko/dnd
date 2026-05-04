import uuid
from jose import JWTError, jwt
from dnd.db.depend import get_db
from dnd.shemas.token import AccessTokenPayload,RefreshTokenPayload
#from urllib3 import request
from jose.exceptions import JWTError, ExpiredSignatureError
#from model.users import User
from datetime import datetime,timedelta,timezone
from dnd.db.user_crud import get_user_rolepermissions
from dnd.core.config import settings
from fastapi import HTTPException,Depends,Request,Response,Header,status
from typing import Optional
from dnd.core.setting import oauth2_scheme
import redis.asyncio as redis
import time
import enum
#from db.depend_redis import get_redis
from dnd.core.logger_config import logg

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
        for perm in roles.permision:
            resurs.append(perm.resource)
    # Стандартные поля payload
    payload = AccessTokenPayload(
        iss="to-dodnd",  # Издатель токена
        sub=str(user.id),  # Собственник токена (UUID пользователя)
        aud=resurs,  # Целевые серверы
        exp=expire,  # Время истечения
        nbf=now,  # Время начала действия
        iat=now,  # Время создания
        jti=jti,  # Уникальный ID токена
        roles=[role.name_role for role in user.roles],  # Кастомные данные
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
    payload = RefreshTokenPayload(
        iss="to-dodnd",  # Издатель токена
        sub=str(user.id),  # Собственник токена (UUID пользователя)
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


async def verify_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        return payload
    except ExpiredSignatureError as e:
        print(f"Токен просрочен: {e}")
        return None
    except JWTError as e:
        print(f"JWT ошибка: {e}")
        print(f"Тип ошибки: {type(e).__name__}")
        # Выводим больше деталей об ошибке
        if "Subject must be a string" in str(e):
            # Декодируем без верификации, чтобы посмотреть что внутри
            try:
                import base64
                import json
                parts = token.split('.')
                if len(parts) == 3:
                    payload_b64 = parts[1]
                    payload_b64 += '=' * (4 - len(payload_b64) % 4)
                    payload_json = base64.urlsafe_b64decode(payload_b64)
                    payload_dict = json.loads(payload_json)
                    print(f"Реальный sub в токене: {payload_dict.get('sub')} (тип: {type(payload_dict.get('sub')).__name__})")
            except:
                pass
        return None
    except Exception as e:
        print(f"Неизвестная ошибка: {e}")
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

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token '{token_type}' not found in Authorization header or cookie",
            headers={"WWW-Authenticate": "Bearer"},
        )

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
