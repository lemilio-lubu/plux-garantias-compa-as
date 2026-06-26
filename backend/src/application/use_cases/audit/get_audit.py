from uuid import UUID

from application.ports.repositories.audit_repository import IAuditRepository
from domain.entities.audit import AuditEntity
from domain.exceptions.base import EntityNotFoundException


class GetAuditUseCase:
    def __init__(self, repository: IAuditRepository) -> None:
        self._repository = repository

    def execute(self, audit_id: UUID) -> AuditEntity:
        audit = self._repository.find_by_id(audit_id)
        if audit is None:
            raise EntityNotFoundException("Audit", str(audit_id))
        return audit
