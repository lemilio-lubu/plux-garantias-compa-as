from typing import List
from uuid import UUID

from application.ports.repositories.srg_body_repository import (
    ISrgEventRepository,
    ISrgPartRepository,
)
from domain.value_objects.srg_event import PartLedger


class GetSrgPartsLedgerUseCase:
    def __init__(
        self,
        part_repo: ISrgPartRepository,
        event_repo: ISrgEventRepository,
    ) -> None:
        self._part_repo = part_repo
        self._event_repo = event_repo

    def execute(self, srg_id: UUID) -> List[dict]:
        parts = self._part_repo.find_by_srg(srg_id)
        counters = self._event_repo.part_counters(srg_id)
        return [
            {"part": part, "ledger": PartLedger.from_counters(part.quantity, counters.get(part.id, {}))}
            for part in parts
        ]
