from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID, uuid4

from .base import BaseEntity


@dataclass
class SrgEventEntity(BaseEntity):
    srg_id: UUID = field(default_factory=uuid4)
    srg_part_id: Optional[UUID] = None
    actor_id: Optional[UUID] = None
    actor_role: str = ""
    event_type: str = ""
    quantity: Optional[int] = None
    state_from: str = ""
    state_to: str = ""
    note: str = ""
    # Read-only labels enriched by the repository for timeline display.
    actor_label: str = ""
    part_label: str = ""
