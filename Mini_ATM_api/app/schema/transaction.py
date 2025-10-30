from pydantic import BaseModel
from datetime import datetime

class TransactionCreate(BaseModel):
    user_id: int
    type: str  # deposit or withdraw
    amount: float

class TransactionOut(BaseModel):
    id: int
    type: str
    amount: float
    timestamp: datetime

    class Config:
        from_attributes = True
