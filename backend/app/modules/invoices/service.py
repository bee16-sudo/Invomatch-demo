# backend/app/modules/invoices/service.py

from datetime import date
from decimal import Decimal
from uuid import UUID
from sqlalchemy.orm import Session

from app.core.exceptions import BusinessRuleError, NotFoundError
from app.modules.clients.repository import ClientRepository
from app.modules.invoices.models import Invoice
from app.modules.invoices.repository import InvoiceRepository
from app.modules.invoices.schemas import InvoiceCreate, InvoiceUpdate

VALID_STATUSES = {"pending", "verified", "paid", "disputed"}

# ── Demo limit ───────────────────────────────────────────────────────────────
DEMO_INVOICE_LIMIT = 1
DEMO_UPGRADE_MSG = (
    "Demo limit reached — maximum 1 invoice in the demo version. "
    "Upgrade to the full version for unlimited invoices: "
    "https://github.com/your-username/invomatch"
)


class InvoiceService:
    def __init__(self, db: Session):
        self.invoice_repo = InvoiceRepository(db)
        self.client_repo = ClientRepository(db)

    def create(self, user_id: UUID, data: InvoiceCreate) -> Invoice:
        # ── Demo limit check ─────────────────────────────────────────────────
        existing_count = self.invoice_repo.count_by_user(user_id)
        if existing_count >= DEMO_INVOICE_LIMIT:
            raise BusinessRuleError(DEMO_UPGRADE_MSG)

        client = self.client_repo.find_by_id_and_user(data.client_id, user_id)
        if not client:
            raise BusinessRuleError("Client not found or does not belong to you")

        if data.due_date < data.issue_date:
            raise BusinessRuleError("Due date must be on or after the issue date")

        existing = self.invoice_repo.find_by_number_and_user(data.invoice_number, user_id)
        if existing:
            raise BusinessRuleError(f"Invoice number '{data.invoice_number}' is already in use")

        invoice = Invoice(
            user_id=user_id,
            client_id=data.client_id,
            invoice_number=data.invoice_number,
            amount=data.amount,
            currency=data.currency,
            issue_date=data.issue_date,
            due_date=data.due_date,
            notes=data.notes,
            status="pending",
        )
        return self.invoice_repo.create(invoice)

    def list(self, user_id: UUID, limit: int = 20, offset: int = 0):
        invoices = self.invoice_repo.find_by_user(user_id, limit, offset)
        total = self.invoice_repo.count_by_user(user_id)
        return invoices, total

    def get(self, user_id: UUID, invoice_id: UUID) -> Invoice:
        invoice = self.invoice_repo.find_by_id(invoice_id, user_id)
        if not invoice:
            raise NotFoundError("Invoice", str(invoice_id))
        return invoice

    def update(self, user_id: UUID, invoice_id: UUID, data: InvoiceUpdate) -> Invoice:
        invoice = self.get(user_id, invoice_id)
        if data.status and data.status not in VALID_STATUSES:
            raise BusinessRuleError(f"Invalid status. Must be one of: {', '.join(VALID_STATUSES)}")
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(invoice, field, value)
        return self.invoice_repo.update(invoice)
