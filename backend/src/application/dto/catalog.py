from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
from uuid import UUID


@dataclass
class CreateCatalogParamDTO:
    param_type: str
    code: str
    name: str
    concesionaria: str


@dataclass
class CreateSparePartDTO:
    catalog_code: str
    name: str
    unit_price: Decimal
    concesionaria: str


@dataclass
class UpdateSparePartDTO:
    id: UUID
    name: Optional[str] = None
    unit_price: Optional[Decimal] = None
