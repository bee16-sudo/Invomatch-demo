# backend/app/modules/dashboard/routes.py

from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import JWTBearer
from app.core.cache import get_cached_dashboard, set_cached_dashboard
from app.modules.invoices.repository import InvoiceRepository
from app.modules.payments.repository import PaymentRepository
from app.modules.clients.repository import ClientRepository

router = APIRouter()
auth = JWTBearer()


@router.get("")
async def get_dashboard(
    payload: dict = Depends(auth),
    db: Session = Depends(get_db),
):
    user_id = payload["sub"]

    cached = await get_cached_dashboard(user_id)
    if cached:
        return cached

    invoice_repo = InvoiceRepository(db)
    payment_repo = PaymentRepository(db)
    client_repo = ClientRepository(db)

    data = {
        "total_invoices": invoice_repo.count_by_user(UUID(user_id)),
        "invoice_status": {
            "pending":  invoice_repo.count_by_status(UUID(user_id), "pending"),
            "verified": invoice_repo.count_by_status(UUID(user_id), "verified"),
            "paid":     invoice_repo.count_by_status(UUID(user_id), "paid"),
            "disputed": invoice_repo.count_by_status(UUID(user_id), "disputed"),
        },
        "total_clients": client_repo.count_by_user(UUID(user_id)),
        "total_collected": str(payment_repo.total_collected_by_user(UUID(user_id))),
    }

    await set_cached_dashboard(user_id, data)
    return data
