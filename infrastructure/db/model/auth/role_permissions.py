from sqlalchemy import Table, Column, ForeignKey
from infrastructure.db.model.core.base import Base

permision_roles = Table(
    "permision_roles",
    Base.metadata,
    Column("id_role", ForeignKey("roles.id"), primary_key=True),
    Column("id_permission", ForeignKey("permision.id"), primary_key=True),
)