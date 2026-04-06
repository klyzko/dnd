from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import os


class Settings(BaseSettings):
    # Основные настройки
    PROJECT_NAME: str = "Smart Todo Planner"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    #token
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int


    # Настройки базы данных (добавим позже)
    DATABASE_URL: Optional[str] = None

    # Настройки Telegram (добавим позже)
    TELEGRAM_BOT_TOKEN: Optional[str] = None

    # Настройки DeepSeek (добавим позже)
    DEEPSEEK_API_KEY: Optional[str] = None
    #Settings_db
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    redis_password: str

    # DATABASE_SQLITE = 'sqlite+aiosqlite:///data/db.sqlite3'
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")

    )

    def get_db_url(self):
        return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")


    def get_redis_url(self):
        return f"redis://:{self.redis_password}@localhost:6379/0"

    def get_time_token(self,type:str):
        if type == "access":
            return self.access_token_expire_minutes
        else:
            return self.refresh_token_expire_days


settings = Settings()
