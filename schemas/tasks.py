from tokenize import String
from sqlalchemy import Column, Integer
from app.db.base import Base


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    date_start = Column(String)
    date_end = Column(String)
    description = Column(String)
    name_quest = Column(String)
    quest = Column(String)

