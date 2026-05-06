from pydantic import BaseModel, EmailStr
from typing import List, Optional

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    profile: str
    document: Optional[str] = None
    phone: Optional[str] = None
    allowed_environments: List[str] = []

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    profile: Optional[str] = None
    status: Optional[str] = None
    allowed_environments: Optional[List[str]] = None
