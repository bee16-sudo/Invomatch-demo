# backend/app/modules/clients/routes.py

from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import NotFoundError
from app.core.security import JWTBearer
from app.modules.clients.schemas import ClientCreate, ClientUpdate, ClientResponse
from app.modules.clients.service import ClientService

router = APIRouter()
auth = JWTBearer()


@router.post("", response_model=ClientResponse, status_code=201)
def create_client(
    data: ClientCreate,
    payload: dict = Depends(auth),
    db: Session = Depends(get_db),
):
    service = ClientService(db)
    client = service.create(UUID(payload["sub"]), data)
    return ClientResponse.model_validate(client)


@router.get("", response_model=List[ClientResponse])
def list_clients(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    payload: dict = Depends(auth),
    db: Session = Depends(get_db),
):
    service = ClientService(db)
    clients, _ = service.list(UUID(payload["sub"]), limit, offset)
    return [ClientResponse.model_validate(c) for c in clients]


@router.get("/{client_id}", response_model=ClientResponse)
def get_client(
    client_id: UUID,
    payload: dict = Depends(auth),
    db: Session = Depends(get_db),
):
    try:
        service = ClientService(db)
        client = service.get(UUID(payload["sub"]), client_id)
        return ClientResponse.model_validate(client)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.patch("/{client_id}", response_model=ClientResponse)
def update_client(
    client_id: UUID,
    data: ClientUpdate,
    payload: dict = Depends(auth),
    db: Session = Depends(get_db),
):
    try:
        service = ClientService(db)
        client = service.update(UUID(payload["sub"]), client_id, data)
        return ClientResponse.model_validate(client)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.delete("/{client_id}", status_code=204)
def delete_client(
    client_id: UUID,
    payload: dict = Depends(auth),
    db: Session = Depends(get_db),
):
    try:
        service = ClientService(db)
        service.delete(UUID(payload["sub"]), client_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
