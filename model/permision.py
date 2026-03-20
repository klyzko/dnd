from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column,relationship
from app.db.base import Base


class Permision(Base):
    __tablename__ = 'permision'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name_permision: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    resource: Mapped[str] = mapped_column(String(255), nullable=False)
    action: Mapped[str] = mapped_column(String(255), nullable=False)  # например: 'create', 'read', 'update', 'delete'

    # Связи
    roles = relationship("RolePermission", back_populates="permission")
