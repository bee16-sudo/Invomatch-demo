# backend/app/modules/payments/schemas.py

from pydantic import BaseModel, Field, UUID4
from decimal import Decimal
from datetime import date, datetime
from typing import Optional


class PaymentCreate(BaseModel):
    invoice_id: UUID4
    amount: Decimal = Field(..., gt=0, decimal_places=2)
    currency: str = Field(default="USD", max_length=3)
    payment_date: date
    reference: Optional[str] = None
    notes: Optional[str] = None


class PaymentResponse(BaseModel):
    id: UUID4
    invoice_id: UUID4
    user_id: UUID4
    amount: Decimal
    currency: str
    payment_date: date
    reference: Optional[str]
    status: str
    notes: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
