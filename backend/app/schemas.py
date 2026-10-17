from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class ContactCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    subject: str = Field(min_length=3, max_length=160)
    message: str = Field(min_length=10, max_length=5000)

class ContactOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str
    subject: str
    message: str
    status: str
    created_at: datetime

class StatusUpdate(BaseModel):
    status: str = Field(pattern="^(new|read|archived)$")

class AdminLogin(BaseModel):
    password: str = Field(min_length=1, max_length=256)

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
