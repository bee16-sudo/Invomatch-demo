# backend/app/modules/invoices/routes.py

from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import BusinessRuleError, NotFoundError
from app.core.security import JWTBearer
from app.modules.invoices.schemas import InvoiceCreate, InvoiceUpdate, InvoiceResponse
from app.modules.invoices.service import InvoiceService

router = APIRouter()
auth = JWTBearer()


@router.post("", response_model=InvoiceResponse, status_code=201)
def create_invoice(
    data: InvoiceCreate,
    payload: dict = Depends(auth),
    db: Session = Depends(get_db),
):
    try:
        service = InvoiceService(db)
        invoice = service.create(UUID(payload["sub"]), data)
        return InvoiceResponse.model_validate(invoice)
    except BusinessRuleError as e:
        raise HTTPException(status_code=422, detail=e.message)


@router.get("", response_model=List[InvoiceResponse])
def list_invoices(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    payload: dict = Depends(auth),
    db: Session = Depends(get_db),
):
    service = InvoiceService(db)
    invoices, _ = service.list(UUID(payload["sub"]), limit, offset)
    return [InvoiceResponse.model_validate(i) for i in invoices]


@router.get("/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(
    invoice_id: UUID,
    payload: dict = Depends(auth),
    db: Session = Depends(get_db),
):
    try:
        service = InvoiceService(db)
        invoice = service.get(UUID(payload["sub"]), invoice_id)
        return InvoiceResponse.model_validate(invoice)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.patch("/{invoice_id}", response_model=InvoiceResponse)
def update_invoice(
    invoice_id: UUID,
    data: InvoiceUpdate,
    payload: dict = Depends(auth),
    db: Session = Depends(get_db),
):
    try:
        service = InvoiceService(db)
        invoice = service.update(UUID(payload["sub"]), invoice_id, data)
        return InvoiceResponse.model_validate(invoice)
    except (NotFoundError, BusinessRuleError) as e:
        raise HTTPException(status_code=404 if isinstance(e, NotFoundError) else 422, detail=e.message)
