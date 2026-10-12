
from sqlalchemy import Boolean, Column, Date, Integer, String, Text
from database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, default="")
    priority = Column(String(20), default="Medium")
    due_date = Column(Date, nullable=True)
    completed = Column(Boolean, default=False)
