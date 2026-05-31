from infrastructure.db.model.auth.users import User
from infrastructure.db.model.game.hero import Hero
from infrastructure.db.model.game.tasks import Task
from infrastructure.db.model.auth.roles import Role
from infrastructure.db.model.auth.permision import Permision

# Экспортируем их
__all__ = ["User", "Hero", "Task", "Role",  "Permision"]