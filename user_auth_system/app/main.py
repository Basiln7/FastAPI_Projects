from fastapi import FastAPI
from app.db.database import engine, Base
from app.api.routes import auth

# create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Auth System - Fresh Start")

app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "User Auth System running"}
