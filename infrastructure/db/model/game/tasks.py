
from sqlalchemy import Integer,String, ForeignKey,Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from infrastructure.db.model.core.base import Base
from typing import Optional


class Task(Base):
    __tablename__ = 'tasks'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    date_start: Mapped[str] = mapped_column(String(255),  nullable=False)
    date_end: Mapped[str] = mapped_column(String(255),  nullable=False)
    description: Mapped[str] = mapped_column(String(1000),  nullable=False)
    name_quest: Mapped[str] = mapped_column(String(255),nullable=True)
    quest: Mapped[str] = mapped_column(String(1000),nullable=True)
    flag_execution: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    health: Mapped[int] = mapped_column(Integer,nullable=True)
    manna: Mapped[int] = mapped_column(Integer,nullable=True)
    power: Mapped[int] = mapped_column(Integer,nullable=True)
    intelligence: Mapped[int] = mapped_column(Integer,nullable=True)
    agility: Mapped[int] = mapped_column(Integer,nullable=True)
    loot: Mapped[str|None] = mapped_column(String(255),nullable=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"),nullable=True)
    user: Mapped[Optional['User']] = relationship("User", back_populates="tasks")