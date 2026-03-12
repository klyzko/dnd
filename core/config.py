from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Основные настройки
    PROJECT_NAME: str = "Smart Todo Planner"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Настройки базы данных (добавим позже)
    DATABASE_URL: Optional[str] = None

    # Настройки Telegram (добавим позже)
    TELEGRAM_BOT_TOKEN: Optional[str] = None

    # Настройки DeepSeek (добавим позже)
    DEEPSEEK_API_KEY: Optional[str] = None

    class Config:
        env_file = ".env"


settings = Settings()