# backend/app/modules/clients/schemas.py

from pydantic import BaseModel, EmailStr, UUID4
from datetime import datetime
from typing import Optional


class ClientCreate(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    tax_id: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None


class ClientUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    tax_id: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None


class ClientResponse(BaseModel):
    id: UUID4
    user_id: UUID4
    name: str
    email: Optional[str]
    tax_id: Optional[str]
    address: Optional[str]
    phone: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
