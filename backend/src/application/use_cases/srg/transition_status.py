from datetime import date
from typing import Optional
from uuid import UUID

from application.dto.srg_body import TransitionSrgStatusDTO
from application.ports.repositories.srg_body_repository import ISrgEventRepository
from application.ports.repositories.srg_repository import ISrgRepository
from domain.entities.srg import SrgEntity
from domain.entities.srg_event import SrgEventEntity
from domain.exceptions.base import EntityNotFoundException
from domain.value_objects.srg_event import SrgEventType
from domain.value_objects.srg_status import SrgStatus


class TransitionSrgStatusUseCase:
    def __init__(
        self,
        repository: ISrgRepository,
        event_repo: Optional[ISrgEventRepository] = None,
    ) -> None:
        self._repository = repository
        self._event_repo = event_repo

    def execute(
        self,
        dto: TransitionSrgStatusDTO,
        actor_id: Optional[UUID] = None,
        actor_role: str = "",
    ) -> SrgEntity:
        srg = self._repository.find_by_id(dto.srg_id)
        if srg is None:
            raise EntityNotFoundException("SRG", str(dto.srg_id))

        previous = srg.status
        new_status = SrgStatus(dto.new_status)
        fecha = date.fromisoformat(dto.fecha_aprobacion) if dto.fecha_aprobacion else None

        srg.transition_to(new_status, fecha_aprobacion=fecha)
        saved = self._repository.save(srg)

        if self._event_repo is not None:
            self._event_repo.save(
                SrgEventEntity(
                    srg_id=srg.id,
                    actor_id=actor_id,
                    actor_role=actor_role,
                    event_type=SrgEventType.STATUS_CHANGED.value,
                    state_from=str(previous),
                    state_to=str(new_status),
                )
            )
        return saved
