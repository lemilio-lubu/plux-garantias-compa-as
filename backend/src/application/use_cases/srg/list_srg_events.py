from typing import List, Optional
from uuid import UUID

from application.ports.repositories.srg_body_repository import ISrgEventRepository
from domain.entities.srg_event import SrgEventEntity


class ListSrgEventsUseCase:
    def __init__(self, event_repo: ISrgEventRepository) -> None:
        self._event_repo = event_repo

    def execute(
        self,
        srg_id: Optional[UUID] = None,
        concesionaria: Optional[str] = None,
        event_type: Optional[str] = None,
    ) -> List[SrgEventEntity]:
        if srg_id is not None:
            return self._event_repo.find_by_srg(srg_id)
        return self._event_repo.search(concesionaria=concesionaria, event_type=event_type)
