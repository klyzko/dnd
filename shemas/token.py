from enum import Enum
from pydantic import BaseModel, Field, field_validator
from datetime import datetime,timezone
from typing import  List, Optional

class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"

class BaseToken(BaseModel):
    iss: str = Field(..., description="Издатель токена (UUID приложения)")
    sub: str = Field(..., description="Собственник токена (UUID пользователя)")
    aud: List[str] = Field(..., description="Массив URL серверов, для которых предназначен токен")
    exp: datetime = Field(..., description="Время истечения токена")
    nbf: datetime = Field(..., description="Время, с которого токен считается валидным")
    iat: datetime = Field(..., description="Время создания токена")
    jti: str = Field(..., description="Уникальный идентификатор токена")


    @field_validator('exp', 'nbf', 'iat', mode='before')
    @classmethod
    def validate_datetime(cls, v):
        """Валидация datetime полей с поддержкой разных форматов"""
        if v is None:
            return v

        # Если уже datetime, возвращаем как есть
        if isinstance(v, datetime):
            return v

        # Если число (int/float) - Unix timestamp
        if isinstance(v, (int, float)):
            return datetime.fromtimestamp(v, tz=timezone.utc)

        # Если строка
        if isinstance(v, str):
            # Попробуем распарсить как число
            try:
                timestamp = float(v)
                return datetime.fromtimestamp(timestamp, tz=timezone.utc)
            except ValueError:
                pass

            # Попробуем ISO формат
            try:
                return datetime.fromisoformat(v.replace('Z', '+00:00'))
            except ValueError:
                raise ValueError(f"Invalid datetime format: {v}")

        raise ValueError(f"Unsupported datetime type: {type(v)}")

class AccessTokenPayload(BaseToken):
        """Структура Access токена"""
        type: TokenType = TokenType.ACCESS
        roles: List[str] = Field(default=[], description="Роли пользователя")
        permissions: List[str] = Field(default=[], description="Разрешения пользователя")


class RefreshTokenPayload(BaseToken):
        """Структура Refresh токена - минимальный набор данных"""
        type: TokenType = TokenType.REFRESH
        session_id: str = Field(..., description="ID сессии")


