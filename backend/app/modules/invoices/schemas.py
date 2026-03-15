# backend/app/modules/invoices/schemas.py

from pydantic import BaseModel, Field, UUID4
from decimal import Decimal
from datetime import date, datetime
from typing import Optional


class InvoiceCreate(BaseModel):
    client_id: UUID4
    invoice_number: str = Field(..., min_length=1, max_length=50)
    amount: Decimal = Field(..., gt=0, decimal_places=2)
    currency: str = Field(default="USD", max_length=3)
    issue_date: date
    due_date: date
    notes: Optional[str] = None


class InvoiceUpdate(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None
    due_date: Optional[date] = None


class InvoiceResponse(BaseModel):
    id: UUID4
    user_id: UUID4
    client_id: UUID4
    invoice_number: str
    amount: Decimal
    currency: str
    status: str
    issue_date: date
    due_date: date
    notes: Optional[str]
    verified_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True
