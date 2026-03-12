from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Создание движка (один на приложение)
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=20,  # для PostgreSQL
    max_overflow=10 # логировать SQL запросы (только для разработки)
)

# Создание фабрики сессий
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Базовый класс для моделей
Base = declarative_base()