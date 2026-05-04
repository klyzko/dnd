from pydantic import BaseModel, Field,ConfigDict,EmailStr,field_validator
from typing import List, Optional




class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: bool = True
    password: str  # ⚠️ Это поле будет в ответах API!
    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    hero_name: str
    @field_validator('password')
    @classmethod
    def validate_and_hash_password(cls, v: str) -> str:
        """Валидация и хеширование пароля"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v


class UserReqwest(BaseModel):
    email: EmailStr
    password: str
    def verify_password(self, plain_password: str, stored_hash: str) -> bool:
        """Проверка пароля (принимает хеш из БД)"""
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            stored_hash.encode('utf-8')
        )

class Charters(BaseModel):
    health: Optional[str] = Field(None,description="жизнь")
    manna: Optional[str] = Field(None,description="мана")
    power: Optional[str] = Field(None,description="сила")
    intelligence: Optional[str] = Field(None,description="интелект")
    agility: Optional[str] = Field(None,description="ловкость")


class Hero(BaseModel):
    logo: str
    inventar: list[str]
    charters: Charters