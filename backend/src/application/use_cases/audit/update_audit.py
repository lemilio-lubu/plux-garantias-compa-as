from application.dto.audit import UpdateAuditDTO
from application.ports.repositories.audit_repository import IAuditRepository
from domain.entities.audit import AuditAttachment, AuditEntity
from domain.exceptions.base import EntityNotFoundException


class UpdateAuditUseCase:
    def __init__(self, repository: IAuditRepository) -> None:
        self._repository = repository

    def execute(self, dto: UpdateAuditDTO) -> AuditEntity:
        audit = self._repository.find_by_id(dto.id)
        if audit is None:
            raise EntityNotFoundException("Audit", str(dto.id))

        if dto.ot_factura is not None:
            audit.ot_factura = dto.ot_factura.upper()
        if dto.observations is not None:
            audit.observations = dto.observations.upper()
        if dto.additional_emails is not None:
            audit.additional_emails = [e.lower() for e in dto.additional_emails]
        if dto.attachments is not None:
            audit.attachments = [
                AuditAttachment(file_name=a.file_name.upper(), file_url=a.file_url)
                for a in dto.attachments
            ]

        return self._repository.save(audit)
