from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from dnd.db.base import Base


class UserRole(Base):
    __tablename__ = 'user_roles'
    id_role: Mapped[int] = mapped_column(ForeignKey('roles.id'),primary_key=True)
    id_user: Mapped[int] = mapped_column(ForeignKey('users.id'),primary_key=True)