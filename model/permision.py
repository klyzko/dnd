from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column,relationship
from dnd.db.base import Base
from typing import List
from dnd.model.role_permissions import permision_roles

class Permision(Base):
    __tablename__ = 'permision'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name_permision: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    resource: Mapped[str] = mapped_column(String(255), nullable=False)
    action: Mapped[str] = mapped_column(String(255), nullable=False)  # например: 'create', 'read', 'update', 'delete'

    # Связи
    roles:Mapped[List['Role']] = relationship("Role", secondary=permision_roles, back_populates="permision")
