from typing import List

from application.ports.repositories.audit_repository import IAuditRepository
from domain.entities.audit import AuditEntity


class ListAuditsUseCase:
    def __init__(self, repository: IAuditRepository) -> None:
        self._repository = repository

    def execute(self, concesionaria: str) -> List[AuditEntity]:
        return self._repository.find_by_concesionaria(concesionaria)
