# backend/app/modules/payments/service.py

from decimal import Decimal
from uuid import UUID
from sqlalchemy.orm import Session

from app.core.exceptions import BusinessRuleError, NotFoundError
from app.modules.invoices.repository import InvoiceRepository
from app.modules.payments.models import Payment
from app.modules.payments.repository import PaymentRepository
from app.modules.payments.schemas import PaymentCreate


class PaymentService:
    def __init__(self, db: Session):
        self.payment_repo = PaymentRepository(db)
        self.invoice_repo = InvoiceRepository(db)

    def record(self, user_id: UUID, data: PaymentCreate) -> Payment:
        # Verify the invoice belongs to the user
        invoice = self.invoice_repo.find_by_id(data.invoice_id, user_id)
        if not invoice:
            raise NotFoundError("Invoice", str(data.invoice_id))

        # Business rule: cannot record payment for disputed invoice
        if invoice.status == "disputed":
            raise BusinessRuleError("Cannot record payment for a disputed invoice")

        # Business rule: payment amount cannot exceed invoice amount
        existing_payments = self.payment_repo.find_by_invoice(data.invoice_id, user_id)
        total_paid = sum(p.amount for p in existing_payments)
        if total_paid + data.amount > invoice.amount:
            raise BusinessRuleError(
                f"Payment would exceed invoice total. Remaining: {invoice.amount - total_paid}"
            )

        payment = Payment(
            invoice_id=data.invoice_id,
            user_id=user_id,
            amount=data.amount,
            currency=data.currency,
            payment_date=data.payment_date,
            reference=data.reference,
            notes=data.notes,
            status="recorded",
        )
        created = self.payment_repo.create(payment)

        # Auto-update invoice to paid if fully settled
        new_total = total_paid + data.amount
        if new_total >= invoice.amount:
            invoice.status = "paid"
            self.invoice_repo.update(invoice)

        return created

    def list_by_invoice(self, user_id: UUID, invoice_id: UUID):
        invoice = self.invoice_repo.find_by_id(invoice_id, user_id)
        if not invoice:
            raise NotFoundError("Invoice", str(invoice_id))
        return self.payment_repo.find_by_invoice(invoice_id, user_id)

    def list_by_user(self, user_id: UUID, limit: int = 20, offset: int = 0):
        return self.payment_repo.find_by_user(user_id, limit, offset)
