from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base
from app.api.v1.routes import user,transaction,auth

app = FastAPI(title="Mini ATM API",
              description="jorny of programmer",
              version="1.1.2")

# Create all tables automatically (will work after we add models)
Base.metadata.create_all(bind=engine)
app.include_router(user.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(transaction.router, prefix="/api/v1/transactions", tags=["Transactions"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])


@app.get("/")
def root():
    return {"message": "Mini ATM API is running 🚀"}
@app.get("health")
def health():
    return {"message":"Mini ATM API is still working!"}