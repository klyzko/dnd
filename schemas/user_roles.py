from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class UserRoles(Base):
    __tablename__ = 'user_roles'
    id_role: Mapped[int] = mapped_column(ForeignKey('roles.id_role'),primary_key=True)
    id_user: Mapped[int] = mapped_column(ForeignKey('users.id_user'),primary_key=True)