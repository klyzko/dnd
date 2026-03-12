# models/__init__.py
from .users import User
from .tasks import Task
from .roles import Role


# Экспортируем все модели
__all__ = ['User', 'Task', 'Role',]