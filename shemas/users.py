from pydantic import BaseModel, Field,ConfigDict,EmailStr
from typing import List, Optional


class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: bool = True
    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    password: str


class UserResponse(UserBase):
    id: int
    is_active: bool


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