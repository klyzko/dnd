from sqlalchemy import String, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from dnd.db.base import Base
from typing import Optional, List



class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    hero: Mapped[Optional["Hero"] ] = relationship(back_populates="user", uselist=False)
    tasks: Mapped[List["Task"]] = relationship(back_populates="user",cascade="all, delete-orphan")
    roles: Mapped[List["Role"]] = relationship(secondary="user_roles", back_populates="users")


