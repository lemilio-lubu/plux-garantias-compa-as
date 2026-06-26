from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID, uuid4

from .base import BaseEntity


@dataclass
class AuditAttachment:
    file_name: str
    file_url: str


@dataclass
class AuditEntity(BaseEntity):
    srg_id: UUID = field(default_factory=uuid4)
    ot_factura: str = ""
    observations: str = ""
    concesionaria: str = ""
    auditor_id: Optional[UUID] = None
    additional_emails: list[str] = field(default_factory=list)
    attachments: list[AuditAttachment] = field(default_factory=list)
