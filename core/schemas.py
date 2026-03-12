from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Transfer Schemas
class TransferPrepareRequest(BaseModel):
    path: str
    operation: str = "upload" # upload | download

class TransferTokenResponse(BaseModel):
    transfer_token: str
    quic_addr: str
    path: str
    expires_in: int
