from sqlalchemy import String, Integer, Enum
from sqlalchemy.orm import Mapped, mapped_column,relationship
from app.db.base import Base
from typing import List

import enum

class Name_role(enum.Enum): # Изменяем на наследование от enum.Enum
    Admin = 'admin'
    User = 'user'
    Reader = 'reader'

class Role(Base):
    __tablename__ = 'roles'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Используем sqlalchemy.Enum для хранения значений из Name_role
    name_role: Mapped[Name_role] = mapped_column(Enum(Name_role, values_callable=lambda obj: [e.value for e in obj]), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True) # Используем Union type для nullable полей
    user: Mapped["Role"] = relationship("Role", secondary="user_roles", back_populates="roles")
    roles: Mapped[List["Role"]] = relationship(secondary="user_roles", back_populates="users")