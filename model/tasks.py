
from sqlalchemy import Column, Integer,String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from typing import Optional


class Task(Base):
    __tablename__ = 'tasks'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    date_start: Mapped[str] = mapped_column(String(255),  nullable=False)
    date_end: Mapped[str] = mapped_column(String(255),  nullable=False)
    description: Mapped[str] = mapped_column(String(255),  nullable=False)
    name_quest: Mapped[str] = mapped_column(String(255),  nullable=False)
    quest: Mapped[str] = mapped_column(String(255),  nullable=False)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"),nullable=True)
    user: Mapped[Optional['User']] = relationship("User", back_populates="tasks")