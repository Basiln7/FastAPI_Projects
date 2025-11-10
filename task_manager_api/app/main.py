from fastapi import FastAPI
from app.db.database import engine
from app.db.database import Base
from app.api.routes import auth,task

app = FastAPI(title="Task Manager API",
              description="just add task",
              version="1.1.2")

# Create all tables automatically (will work after we add models)
# main.py or wherever Base.metadata.create_all(engine) exists
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(task.router, prefix="/api/task", tags=["Task"])



@app.get("/")
def root():
    return {"message": "Task Adding API is running 🚀"}
@app.get("health")
def health():
    return {"message":"Task API is still working!"}