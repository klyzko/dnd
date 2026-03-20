from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class RolePermissions(Base):
    __tablename__ = 'user_roles'
    id_role: Mapped[int] = mapped_column(ForeignKey('roles.id'),primary_key=True)
    id_permission: Mapped[int] = mapped_column(ForeignKey('permissions.id'),primary_key=True)