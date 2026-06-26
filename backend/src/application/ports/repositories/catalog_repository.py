from abc import abstractmethod
from typing import List, Optional

from .base import IRepository
from domain.entities.catalog import CatalogParamEntity, SparePartEntity


class ICatalogParamRepository(IRepository[CatalogParamEntity]):
    @abstractmethod
    def find_by_type_and_concesionaria(
        self, param_type: str, concesionaria: str
    ) -> List[CatalogParamEntity]: ...

    @abstractmethod
    def exists(self, param_type: str, code: str, concesionaria: str) -> bool: ...


class ISparePartRepository(IRepository[SparePartEntity]):
    @abstractmethod
    def find_by_concesionaria(self, concesionaria: str) -> List[SparePartEntity]: ...

    @abstractmethod
    def find_by_catalog_code(
        self, catalog_code: str, concesionaria: str
    ) -> Optional[SparePartEntity]: ...

    @abstractmethod
    def exists_by_code(self, catalog_code: str, concesionaria: str) -> bool: ...
