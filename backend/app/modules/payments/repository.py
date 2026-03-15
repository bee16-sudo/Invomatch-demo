# backend/app/modules/payments/repository.py

from typing import List, Optional
from uuid import UUID
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.modules.payments.models import Payment


class PaymentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, payment: Payment) -> Payment:
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        return payment

    def find_by_id(self, payment_id: UUID, user_id: UUID) -> Optional[Payment]:
        return self.db.query(Payment).filter(
            Payment.id == payment_id,
            Payment.user_id == user_id,
        ).first()

    def find_by_invoice(self, invoice_id: UUID, user_id: UUID) -> List[Payment]:
        return self.db.query(Payment).filter(
            Payment.invoice_id == invoice_id,
            Payment.user_id == user_id,
        ).order_by(Payment.payment_date.desc()).all()

    def find_by_user(self, user_id: UUID, limit: int = 20, offset: int = 0) -> List[Payment]:
        return self.db.query(Payment).filter(
            Payment.user_id == user_id
        ).order_by(Payment.created_at.desc()).limit(limit).offset(offset).all()

    def total_collected_by_user(self, user_id: UUID) -> Decimal:
        result = self.db.query(func.sum(Payment.amount)).filter(
            Payment.user_id == user_id,
            Payment.status == "recorded",
        ).scalar()
        return result or Decimal("0")
