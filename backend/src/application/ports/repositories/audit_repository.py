from abc import abstractmethod
from typing import List, Optional
from uuid import UUID

from .base import IRepository
from domain.entities.audit import AuditEntity


class IAuditRepository(IRepository[AuditEntity]):
    @abstractmethod
    def find_by_srg(self, srg_id: UUID) -> Optional[AuditEntity]: ...

    @abstractmethod
    def find_by_concesionaria(self, concesionaria: str) -> List[AuditEntity]: ...
