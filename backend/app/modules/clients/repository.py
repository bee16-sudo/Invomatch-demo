# backend/app/modules/clients/repository.py

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.modules.clients.models import Client


class ClientRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, client: Client) -> Client:
        self.db.add(client)
        self.db.commit()
        self.db.refresh(client)
        return client

    def find_by_id_and_user(self, client_id: UUID, user_id: UUID) -> Optional[Client]:
        return self.db.query(Client).filter(
            Client.id == client_id,
            Client.user_id == user_id,
        ).first()

    def find_by_user(self, user_id: UUID, limit: int = 20, offset: int = 0) -> List[Client]:
        return self.db.query(Client).filter(
            Client.user_id == user_id
        ).order_by(Client.created_at.desc()).limit(limit).offset(offset).all()

    def count_by_user(self, user_id: UUID) -> int:
        return self.db.query(Client).filter(Client.user_id == user_id).count()

    def update(self, client: Client) -> Client:
        self.db.commit()
        self.db.refresh(client)
        return client

    def delete(self, client: Client) -> None:
        self.db.delete(client)
        self.db.commit()
