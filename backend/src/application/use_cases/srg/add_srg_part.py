from typing import Optional
from uuid import UUID

from application.dto.srg_body import AddSrgPartDTO
from application.ports.repositories.srg_body_repository import (
    ISrgEventRepository,
    ISrgPartRepository,
)
from application.ports.repositories.srg_repository import ISrgRepository
from domain.entities.srg_event import SrgEventEntity
from domain.entities.srg_part import SrgPartEntity
from domain.exceptions.base import BusinessRuleViolationException, EntityNotFoundException
from domain.value_objects.srg_event import SrgEventType
from domain.value_objects.srg_type import SrgType


class AddSrgPartUseCase:
    def __init__(
        self,
        srg_repo: ISrgRepository,
        part_repo: ISrgPartRepository,
        event_repo: ISrgEventRepository,
    ) -> None:
        self._srg_repo = srg_repo
        self._part_repo = part_repo
        self._event_repo = event_repo

    def execute(
        self,
        dto: AddSrgPartDTO,
        actor_id: Optional[UUID] = None,
        actor_role: str = "",
    ) -> SrgPartEntity:
        srg = self._srg_repo.find_by_id(dto.srg_id)
        if srg is None:
            raise EntityNotFoundException("SRG", str(dto.srg_id))
        if srg.srg_type != SrgType.WARRANTY:
            raise BusinessRuleViolationException("Solo las garantías admiten repuestos.")

        part = SrgPartEntity(
            srg_id=dto.srg_id,
            catalog_code=dto.catalog_code.upper(),
            name_es=dto.name_es.upper(),
            quantity=dto.quantity,
            unit_price=dto.unit_price,
            part_origin=dto.part_origin.upper(),
            invoice_number=dto.invoice_number.upper(),
        )
        saved = self._part_repo.save(part)

        self._event_repo.save(
            SrgEventEntity(
                srg_id=dto.srg_id,
                srg_part_id=saved.id,
                actor_id=actor_id,
                actor_role=actor_role,
                event_type=SrgEventType.PART_REQUESTED.value,
                quantity=saved.quantity,
                note=f"{saved.catalog_code} x{saved.quantity}",
            )
        )
        return saved
