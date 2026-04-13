from sqlalchemy import Column, Integer, String, ForeignKey,JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from dnd.db.base import Base
from typing import Optional, List,Any


class Hero(Base):
    __tablename__ = "heros"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    health: Mapped[int] = mapped_column(Integer, nullable=False)
    manna: Mapped[int] = mapped_column(Integer, nullable=False)
    power: Mapped[int] = mapped_column(Integer, nullable=False)
    intelligence: Mapped[int] = mapped_column(Integer, nullable=False)
    agility: Mapped[int] = mapped_column(Integer, nullable=False)
    inventory: Mapped[Optional[List[Any]]] = mapped_column(JSON, default=list)

    # Внешний ключ к User (с unique=True для one-to-one)
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),  # ссылаемся на users.id, а не id_user
        unique=True,  # Важно для one-to-one
        nullable=True
    )

    # Связь с User
    user: Mapped[Optional["User"]] = relationship(
        back_populates="hero"
    )
