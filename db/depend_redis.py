import redis.asyncio as redis
from contextlib import asynccontextmanager
from dnd.core.config import settings
from fastapi import FastAPI


redis_client: redis.Redis = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Запускается при старте и остановке приложения"""
    global redis_client

    # Открываем соединение при старте
    url=settings.get_redis_url()
    redis_client = await redis.from_url(
        url,
        decode_responses=True
    )
    #print("✅ Redis connected")

    yield

    # Закрываем соединение при остановке
    if redis_client:
        await redis_client.close()
        await redis_client.connection_pool.disconnect()
        #print("❌ Redis disconnected")


async def get_redis() -> redis.Redis:
    """Возвращает Redis клиент (один на всё приложение)"""
    return redis_client