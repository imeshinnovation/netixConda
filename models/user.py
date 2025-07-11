# user.py (modelo)
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    name: str
    lastname: str
    email: EmailStr  # Valida formato email automáticamente
    password: str

    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        return v

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[str] = None
    lastname: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

class UserDB(UserBase):
    created_at: datetime = datetime.utcnow()
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str