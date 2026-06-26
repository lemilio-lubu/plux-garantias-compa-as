from dataclasses import dataclass, field
from uuid import UUID, uuid4

from .base import BaseEntity


@dataclass
class CampaignBodyEntity(BaseEntity):
    srg_id: UUID = field(default_factory=uuid4)
    update_name: str = ""
    image_link: str = ""
    modified_by: str = ""
