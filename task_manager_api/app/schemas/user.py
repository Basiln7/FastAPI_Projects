from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr

class LoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True
