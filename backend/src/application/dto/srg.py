from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class CreateWarrantySrgDTO:
    concesionaria: str
    asesor_id: UUID
    ot: str
    vin: str
    placa: str
    vehicle_model: str
    vehicle_color: str
    vehicle_year: int
    km_apertura: int
    sede: str
    nro_garantia: str
    warranty_type_code: str
    warranty_type_name: str


@dataclass
class CreateCampaignSrgDTO:
    concesionaria: str
    asesor_id: UUID
    ot: str
    vin: str
    placa: str
    vehicle_model: str
    vehicle_year: int
    km_apertura: int
    sede: str
    campaign_code: str


@dataclass
class SearchSrgDTO:
    concesionaria: str
    ot: Optional[str] = None
    vin: Optional[str] = None
    sede: Optional[str] = None
