from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import Task
from app.db.models import User
from app.schemas.task import TaskCreate, TaskOut

router = APIRouter()
def get_current_user(db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == TaskCreate.user_id).first()

@router.post("/operate", response_model=TaskOut)
def handle_task(data: TaskCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    task = Task(user_id=user.id, task_name=data.task_name, task_description=data.task_description)
    db.add(task)
    db.commit()
    db.refresh(task)
    db.refresh(user)
    return task

@router.get("/{user_id}/history", response_model=list[TaskOut])
def transaction_history(user_id: int, db: Session = Depends(get_db)):
    return db.query(Task).filter(Task.user_id == user_id).all()

# ✅ Update Task
@router.put("/{task_id}", response_model=TaskOut)
def update_task(task_id: int, task_update: TaskCreate, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.task_name = task_update.task_name
    task.task_description = task_update.task_description

    db.commit()
    db.refresh(task)
    return task


# ✅ Delete Task
@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}

