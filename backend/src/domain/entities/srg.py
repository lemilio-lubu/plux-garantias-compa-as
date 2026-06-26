from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional
from uuid import UUID

from .base import BaseEntity
from domain.value_objects.srg_status import SrgStatus
from domain.value_objects.srg_type import SrgType
from domain.exceptions.base import BusinessRuleViolationException


@dataclass
class SrgEntity(BaseEntity):
    ot: str = ""
    srg_type: SrgType = SrgType.WARRANTY
    status: SrgStatus = SrgStatus.PROCESO
    concesionaria: str = ""
    asesor_id: Optional[UUID] = None

    # Common header fields
    vin: str = ""
    vehicle_model: str = ""
    vehicle_color: str = ""
    vehicle_year: int = 0
    km_apertura: int = 0
    sede: str = ""

    # Warranty-specific
    nro_garantia: Optional[str] = None
    warranty_type_code: Optional[str] = None
    warranty_type_name: Optional[str] = None

    # Campaign-specific
    campaign_code: Optional[str] = None

    # Status timestamps
    fecha_envio_marca: Optional[datetime] = None
    fecha_aprobacion: Optional[date] = None

    @property
    def checklist_enabled(self) -> bool:
        # The parts checklist becomes available once the SRG is sent to the brand
        # and stays available through the approval pipeline.
        return self.status in (
            SrgStatus.PENDIENTE,
            SrgStatus.PREAPROBADO,
            SrgStatus.APROBADO,
        )

    @property
    def campaign_body_enabled(self) -> bool:
        # The campaign body is only registered once the campaign is approved.
        return self.status == SrgStatus.APROBADO

    def transition_to(self, new_status: SrgStatus, fecha_aprobacion: Optional[date] = None) -> None:
        from datetime import datetime, timezone

        # Campaigns can be approved directly from PROCESO (skipping PENDIENTE/PREAPROBADO)
        campaign_direct_approve = (
            self.srg_type == SrgType.CAMPAIGN
            and self.status == SrgStatus.PROCESO
            and new_status == SrgStatus.APROBADO
        )
        if not campaign_direct_approve and not self.status.can_transition_to(new_status):
            raise BusinessRuleViolationException(
                f"Cannot transition SRG from {self.status} to {new_status}"
            )
        self.status = new_status
        if new_status == SrgStatus.PENDIENTE:
            self.fecha_envio_marca = datetime.now(timezone.utc)
        if new_status == SrgStatus.APROBADO and fecha_aprobacion:
            self.fecha_aprobacion = fecha_aprobacion
