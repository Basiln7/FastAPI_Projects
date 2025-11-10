from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import User
from app.schemas.user import UserCreate, UserResponse, LoginSchema
from app.core.security import hash_password, verify_password, create_access_token
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/auth", tags=["auth"])



@router.post("/register", response_model=UserResponse, status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    exists = db.query(User).filter(User.email == user.email).first()
                               # models email == Schemas email
    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = hash_password(user.password)
    db_user = User(email=user.email, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login")
def login(payload: LoginSchema, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == payload.email).first()
    if not db_user or not verify_password(payload.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token({"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.get("/me", response_model=UserResponse)
def me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    from jose import jwt, JWTError
    from app.core.config import settings

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user
