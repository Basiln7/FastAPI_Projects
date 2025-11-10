from pydantic import BaseModel
from datetime import datetime


class TaskCreate(BaseModel):
    user_id: int
    task_name: str
    task_description: str

class TaskOut(BaseModel):
    id: int
    task_name: str
    task_description: str
    timestamp: datetime

    class Config:
        from_attributes = True
