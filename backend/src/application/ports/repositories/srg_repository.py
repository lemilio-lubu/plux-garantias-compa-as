from abc import abstractmethod
from typing import List, Optional

from .base import IRepository
from domain.entities.srg import SrgEntity


class ISrgRepository(IRepository[SrgEntity]):
    @abstractmethod
    def find_by_ot(self, ot: str) -> Optional[SrgEntity]: ...

    @abstractmethod
    def find_by_concesionaria(self, concesionaria: str) -> List[SrgEntity]: ...

    @abstractmethod
    def search(
        self,
        concesionaria: str,
        ot: Optional[str] = None,
        vin: Optional[str] = None,
        sede: Optional[str] = None,
    ) -> List[SrgEntity]: ...

    @abstractmethod
    def next_correlativo(self, concesionaria: str, year: int) -> int: ...

    @abstractmethod
    def get_dashboard_stats(self, concesionaria: str) -> List[dict]: ...
    """Returns list of {srg_type, status, count} dicts."""
