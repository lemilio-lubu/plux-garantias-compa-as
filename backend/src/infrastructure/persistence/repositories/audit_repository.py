from typing import List, Optional
from uuid import UUID
from datetime import datetime, timezone

from application.ports.repositories.audit_repository import IAuditRepository
from domain.entities.audit import AuditAttachment, AuditEntity
from infrastructure.persistence.models.audit import Audit


class DjangoAuditRepository(IAuditRepository):
    def find_by_id(self, id: UUID) -> Optional[AuditEntity]:
        try:
            return self._to_entity(Audit.objects.get(id=id, deleted_at__isnull=True))
        except Audit.DoesNotExist:
            return None

    def find_all(self) -> List[AuditEntity]:
        return [self._to_entity(a) for a in Audit.objects.filter(deleted_at__isnull=True)]

    def find_by_srg(self, srg_id: UUID) -> Optional[AuditEntity]:
        try:
            return self._to_entity(Audit.objects.get(srg_id=srg_id, deleted_at__isnull=True))
        except Audit.DoesNotExist:
            return None

    def find_by_concesionaria(self, concesionaria: str) -> List[AuditEntity]:
        return [
            self._to_entity(a)
            for a in Audit.objects.filter(
                concesionaria=concesionaria, deleted_at__isnull=True
            ).select_related("srg")
        ]

    def save(self, entity: AuditEntity) -> AuditEntity:
        attachments_data = [
            {"file_name": a.file_name, "file_url": a.file_url}
            for a in entity.attachments
        ]
        obj, _ = Audit.objects.update_or_create(
            id=entity.id,
            defaults={
                "srg_id": entity.srg_id,
                "ot_factura": entity.ot_factura,
                "observations": entity.observations,
                "concesionaria": entity.concesionaria,
                "auditor_id": entity.auditor_id,
                "additional_emails": entity.additional_emails,
                "attachments": attachments_data,
            },
        )
        return self._to_entity(obj)

    def delete(self, id: UUID) -> None:
        Audit.objects.filter(id=id).update(deleted_at=datetime.now(timezone.utc))

    @staticmethod
    def _to_entity(m: Audit) -> AuditEntity:
        return AuditEntity(
            id=m.id,
            srg_id=m.srg_id,
            ot_factura=m.ot_factura,
            observations=m.observations,
            concesionaria=m.concesionaria,
            auditor_id=m.auditor_id,
            additional_emails=m.additional_emails or [],
            attachments=[
                AuditAttachment(file_name=a["file_name"], file_url=a["file_url"])
                for a in (m.attachments or [])
            ],
            created_at=m.created_at,
            updated_at=m.updated_at,
            deleted_at=m.deleted_at,
        )
