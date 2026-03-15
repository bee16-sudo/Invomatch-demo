# backend/app/modules/invoices/repository.py

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.modules.invoices.models import Invoice


class InvoiceRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, invoice: Invoice) -> Invoice:
        self.db.add(invoice)
        self.db.commit()
        self.db.refresh(invoice)
        return invoice

    def find_by_id(self, invoice_id: UUID, user_id: UUID) -> Optional[Invoice]:
        return self.db.query(Invoice).filter(
            Invoice.id == invoice_id,
            Invoice.user_id == user_id,
        ).first()

    def find_by_id_internal(self, invoice_id: UUID) -> Optional[Invoice]:
        """Used by workers — no user scoping."""
        return self.db.query(Invoice).filter(Invoice.id == invoice_id).first()

    def find_by_number_and_user(self, invoice_number: str, user_id: UUID) -> Optional[Invoice]:
        return self.db.query(Invoice).filter(
            Invoice.invoice_number == invoice_number,
            Invoice.user_id == user_id,
        ).first()

    def find_by_user(self, user_id: UUID, limit: int = 20, offset: int = 0) -> List[Invoice]:
        return self.db.query(Invoice).filter(
            Invoice.user_id == user_id
        ).order_by(Invoice.created_at.desc()).limit(limit).offset(offset).all()

    def count_by_user(self, user_id: UUID) -> int:
        return self.db.query(Invoice).filter(Invoice.user_id == user_id).count()

    def count_by_status(self, user_id: UUID, status: str) -> int:
        return self.db.query(Invoice).filter(
            Invoice.user_id == user_id,
            Invoice.status == status,
        ).count()

    def update(self, invoice: Invoice) -> Invoice:
        self.db.commit()
        self.db.refresh(invoice)
        return invoice
