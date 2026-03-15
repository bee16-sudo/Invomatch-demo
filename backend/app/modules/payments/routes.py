# backend/app/modules/payments/routes.py

from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import BusinessRuleError, NotFoundError
from app.core.security import JWTBearer
from app.modules.payments.schemas import PaymentCreate, PaymentResponse
from app.modules.payments.service import PaymentService

router = APIRouter()
auth = JWTBearer()


@router.post("", response_model=PaymentResponse, status_code=201)
def record_payment(
    data: PaymentCreate,
    payload: dict = Depends(auth),
    db: Session = Depends(get_db),
):
    try:
        service = PaymentService(db)
        payment = service.record(UUID(payload["sub"]), data)
        return PaymentResponse.model_validate(payment)
    except (BusinessRuleError, NotFoundError) as e:
        code = 422 if isinstance(e, BusinessRuleError) else 404
        raise HTTPException(status_code=code, detail=e.message)


@router.get("", response_model=List[PaymentResponse])
def list_payments(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    payload: dict = Depends(auth),
    db: Session = Depends(get_db),
):
    service = PaymentService(db)
    payments = service.list_by_user(UUID(payload["sub"]), limit, offset)
    return [PaymentResponse.model_validate(p) for p in payments]


@router.get("/invoice/{invoice_id}", response_model=List[PaymentResponse])
def list_payments_for_invoice(
    invoice_id: UUID,
    payload: dict = Depends(auth),
    db: Session = Depends(get_db),
):
    try:
        service = PaymentService(db)
        payments = service.list_by_invoice(UUID(payload["sub"]), invoice_id)
        return [PaymentResponse.model_validate(p) for p in payments]
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
