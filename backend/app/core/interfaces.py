# backend/app/core/interfaces.py

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional
from uuid import UUID

T = TypeVar("T")


class Repository(ABC, Generic[T]):
    @abstractmethod
    def create(self, entity: T) -> T: ...

    @abstractmethod
    def find_by_id(self, id: UUID) -> Optional[T]: ...

    @abstractmethod
    def find_all(self, limit: int, offset: int) -> List[T]: ...
