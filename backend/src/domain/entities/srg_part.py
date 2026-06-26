from dataclasses import dataclass, field
from decimal import Decimal
from uuid import UUID, uuid4

from .base import BaseEntity


@dataclass
class SrgPartEntity(BaseEntity):
    srg_id: UUID = field(default_factory=uuid4)
    catalog_code: str = ""
    name_es: str = ""
    quantity: int = 1
    unit_price: Decimal = field(default_factory=lambda: Decimal("0.00"))
    part_origin: str = ""
    invoice_number: str = ""
