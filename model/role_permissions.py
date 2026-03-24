from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from dnd.db.base import Base


class RolePermissions(Base):
    __tablename__ = 'permision_roles'
    id_role: Mapped[int] = mapped_column(ForeignKey('roles.id'),primary_key=True)
    id_permission: Mapped[int] = mapped_column(ForeignKey('permision.id'),primary_key=True)