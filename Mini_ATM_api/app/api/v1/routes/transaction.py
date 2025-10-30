from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.transaction import Transaction
from app.models.user import User
from app.schema.transaction import TransactionCreate, TransactionOut

router = APIRouter()

@router.post("/operate", response_model=TransactionOut)
def handle_transaction(data: TransactionCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if data.type == "deposit":
        user.balance += data.amount
    elif data.type == "withdraw":
        if user.balance < data.amount:
            raise HTTPException(status_code=400, detail="Insufficient balance")
        user.balance -= data.amount
    else:
        raise HTTPException(status_code=400, detail="Invalid transaction type")

    transaction = Transaction(user_id=user.id, type=data.type, amount=data.amount)
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    db.refresh(user)
    return transaction


@router.get("/{user_id}/balance")
def get_balance(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": user.name, "balance": user.balance}


@router.get("/{user_id}/history", response_model=list[TransactionOut])
def transaction_history(user_id: int, db: Session = Depends(get_db)):
    return db.query(Transaction).filter(Transaction.user_id == user_id).all()
