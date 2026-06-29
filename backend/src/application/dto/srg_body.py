from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
from uuid import UUID


@dataclass
class AddSrgPartDTO:
    srg_id: UUID
    catalog_code: str
    name_es: str
    quantity: int
    unit_price: Decimal
    part_origin: str
    invoice_number: str


@dataclass
class RegisterPartMovementDTO:
    srg_id: UUID
    part_id: UUID
    event_type: str
    quantity: int
    actor_id: UUID
    actor_role: str
    note: str = ""
    location: str = ""


@dataclass
class TransitionSrgStatusDTO:
    srg_id: UUID
    new_status: str
    fecha_aprobacion: Optional[str] = None  # ISO date string


@dataclass
class UpsertCampaignBodyDTO:
    srg_id: UUID
    update_name: str
    image_link: str
    modified_by: str
