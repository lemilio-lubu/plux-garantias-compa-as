from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID


@dataclass
class AuditAttachmentDTO:
    file_name: str
    file_url: str


@dataclass
class CreateAuditDTO:
    srg_id: UUID
    ot_factura: str
    observations: str
    auditor_id: UUID
    concesionaria: str
    additional_emails: list[str] = field(default_factory=list)
    attachments: list[AuditAttachmentDTO] = field(default_factory=list)


@dataclass
class UpdateAuditDTO:
    id: UUID
    ot_factura: Optional[str] = None
    observations: Optional[str] = None
    additional_emails: Optional[list[str]] = None
    attachments: Optional[list[AuditAttachmentDTO]] = None
