from abc import abstractmethod
from typing import Dict, List, Optional
from uuid import UUID

from .base import IRepository
from domain.entities.srg_part import SrgPartEntity
from domain.entities.srg_event import SrgEventEntity
from domain.entities.campaign_body import CampaignBodyEntity


class ISrgPartRepository(IRepository[SrgPartEntity]):
    @abstractmethod
    def find_by_srg(self, srg_id: UUID) -> List[SrgPartEntity]: ...


class ISrgEventRepository(IRepository[SrgEventEntity]):
    @abstractmethod
    def find_by_srg(self, srg_id: UUID) -> List[SrgEventEntity]: ...

    @abstractmethod
    def part_counters(self, srg_id: UUID) -> Dict[UUID, Dict[str, int]]:
        """Per part_id, summed quantities keyed by ledger counter name."""
        ...

    @abstractmethod
    def search(
        self,
        concesionaria: Optional[str] = None,
        event_type: Optional[str] = None,
    ) -> List[SrgEventEntity]: ...


class ICampaignBodyRepository(IRepository[CampaignBodyEntity]):
    @abstractmethod
    def find_by_srg(self, srg_id: UUID) -> Optional[CampaignBodyEntity]: ...
