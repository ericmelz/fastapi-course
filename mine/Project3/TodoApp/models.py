from sqlalchemy import Column, Integer, String, Boolean

from database import Base


class TodoList(Base):
    __tablename__ = "todolist"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    status = Column(Boolean, default=False)