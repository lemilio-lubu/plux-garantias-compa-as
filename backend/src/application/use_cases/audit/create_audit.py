from application.dto.audit import CreateAuditDTO
from application.ports.repositories.audit_repository import IAuditRepository
from application.ports.repositories.srg_repository import ISrgRepository
from domain.entities.audit import AuditAttachment, AuditEntity
from domain.exceptions.base import EntityNotFoundException, ValidationException


class CreateAuditUseCase:
    def __init__(self, audit_repo: IAuditRepository, srg_repo: ISrgRepository) -> None:
        self._audit_repo = audit_repo
        self._srg_repo = srg_repo

    def execute(self, dto: CreateAuditDTO) -> AuditEntity:
        srg = self._srg_repo.find_by_id(dto.srg_id)
        if srg is None:
            raise EntityNotFoundException("SRG", str(dto.srg_id))

        if srg.concesionaria != dto.concesionaria:
            raise ValidationException(
                f"SRG {srg.ot} does not belong to concesionaria {dto.concesionaria}"
            )

        entity = AuditEntity(
            srg_id=dto.srg_id,
            ot_factura=dto.ot_factura.upper(),
            observations=dto.observations.upper(),
            concesionaria=dto.concesionaria,
            auditor_id=dto.auditor_id,
            additional_emails=[e.lower() for e in dto.additional_emails],
            attachments=[
                AuditAttachment(file_name=a.file_name.upper(), file_url=a.file_url)
                for a in dto.attachments
            ],
        )
        return self._audit_repo.save(entity)
