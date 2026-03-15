# backend/app/modules/clients/service.py

from uuid import UUID
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError, BusinessRuleError
from app.modules.clients.models import Client
from app.modules.clients.repository import ClientRepository
from app.modules.clients.schemas import ClientCreate, ClientUpdate

# ── Demo limit ────────────────────────────────────────────────────────────────
DEMO_CLIENT_LIMIT = 1
DEMO_UPGRADE_MSG = (
    "Demo limit reached — maximum 1 client in the demo version. "
    "Upgrade to the full version for unlimited clients: "
    "https://github.com/your-username/invomatch"
)


class ClientService:
    def __init__(self, db: Session):
        self.repo = ClientRepository(db)

    def create(self, user_id: UUID, data: ClientCreate) -> Client:
        # ── Demo limit check ──────────────────────────────────────────────────
        existing_count = self.repo.count_by_user(user_id)
        if existing_count >= DEMO_CLIENT_LIMIT:
            raise BusinessRuleError(DEMO_UPGRADE_MSG)

        client = Client(user_id=user_id, **data.model_dump(exclude_none=False))
        return self.repo.create(client)

    def list(self, user_id: UUID, limit: int = 20, offset: int = 0):
        clients = self.repo.find_by_user(user_id, limit, offset)
        total = self.repo.count_by_user(user_id)
        return clients, total

    def get(self, user_id: UUID, client_id: UUID) -> Client:
        client = self.repo.find_by_id_and_user(client_id, user_id)
        if not client:
            raise NotFoundError("Client", str(client_id))
        return client

    def update(self, user_id: UUID, client_id: UUID, data: ClientUpdate) -> Client:
        client = self.get(user_id, client_id)
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(client, field, value)
        return self.repo.update(client)

    def delete(self, user_id: UUID, client_id: UUID) -> None:
        client = self.get(user_id, client_id)
        self.repo.delete(client)
