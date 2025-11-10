from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from datetime import datetime
from app.db.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True, autoincrement=True)
    task_name = Column(String, unique=True, nullable=False)
    task_description= Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("user.id"))

    user=relationship("User", backref="tasks")