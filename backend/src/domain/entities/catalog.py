from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional

from .base import BaseEntity


@dataclass
class CatalogParamEntity(BaseEntity):
    """Reusable catalog parameter (vehicle model, color, warranty type, campaign code)."""
    param_type: str = ""
    code: str = ""
    name: str = ""
    concesionaria: str = ""


@dataclass
class SparePartEntity(BaseEntity):
    catalog_code: str = ""
    name: str = ""
    unit_price: Decimal = field(default_factory=lambda: Decimal("0.00"))
    concesionaria: str = ""
