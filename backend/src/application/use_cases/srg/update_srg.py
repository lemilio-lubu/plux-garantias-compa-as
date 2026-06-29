from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from application.ports.repositories.srg_repository import ISrgRepository
from domain.entities.srg import SrgEntity
from domain.exceptions.base import BusinessRuleViolationException, EntityNotFoundException
from domain.value_objects.srg_status import SrgStatus


EDITABLE_STATUSES = {SrgStatus.PROCESO, SrgStatus.RETORNADO}


@dataclass
class UpdateSrgDTO:
    id: UUID
    # Common
    vin: Optional[str] = None
    placa: Optional[str] = None
    vehicle_model: Optional[str] = None
    vehicle_color: Optional[str] = None
    vehicle_year: Optional[int] = None
    km_apertura: Optional[int] = None
    sede: Optional[str] = None
    # Warranty
    nro_garantia: Optional[str] = None
    warranty_type_code: Optional[str] = None
    warranty_type_name: Optional[str] = None
    # Campaign
    campaign_code: Optional[str] = None


class UpdateSrgUseCase:
    def __init__(self, repository: ISrgRepository) -> None:
        self._repository = repository

    def execute(self, dto: UpdateSrgDTO) -> SrgEntity:
        srg = self._repository.find_by_id(dto.id)
        if srg is None:
            raise EntityNotFoundException("SRG", str(dto.id))

        if srg.status not in EDITABLE_STATUSES:
            raise BusinessRuleViolationException(
                f"SRG in status {srg.status} cannot be edited. "
                f"Allowed: {', '.join(s.value for s in EDITABLE_STATUSES)}"
            )

        str_fields = [
            "vin", "placa", "vehicle_model", "vehicle_color", "sede",
            "nro_garantia", "warranty_type_code", "warranty_type_name",
            "campaign_code",
        ]
        int_fields = ["vehicle_year", "km_apertura"]

        for field_name in str_fields:
            value = getattr(dto, field_name)
            if value is not None:
                setattr(srg, field_name, value.upper())

        for field_name in int_fields:
            value = getattr(dto, field_name)
            if value is not None:
                setattr(srg, field_name, value)

        return self._repository.save(srg)
