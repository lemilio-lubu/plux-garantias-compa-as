from typing import List, Optional
from uuid import UUID
from datetime import datetime, timezone

from application.ports.repositories.catalog_repository import (
    ICatalogParamRepository,
    ISparePartRepository,
)
from domain.entities.catalog import CatalogParamEntity, SparePartEntity
from infrastructure.persistence.models.catalog import CatalogParam, SparePart


class DjangoCatalogParamRepository(ICatalogParamRepository):
    def find_by_id(self, id: UUID) -> Optional[CatalogParamEntity]:
        try:
            return self._to_entity(CatalogParam.objects.get(id=id, deleted_at__isnull=True))
        except CatalogParam.DoesNotExist:
            return None

    def find_all(self) -> List[CatalogParamEntity]:
        return [self._to_entity(p) for p in CatalogParam.objects.filter(deleted_at__isnull=True)]

    def find_by_type_and_concesionaria(
        self, param_type: str, concesionaria: str
    ) -> List[CatalogParamEntity]:
        return [
            self._to_entity(p)
            for p in CatalogParam.objects.filter(
                param_type=param_type, concesionaria=concesionaria, deleted_at__isnull=True
            )
        ]

    def exists(self, param_type: str, code: str, concesionaria: str) -> bool:
        return CatalogParam.objects.filter(
            param_type=param_type, code=code, concesionaria=concesionaria, deleted_at__isnull=True
        ).exists()

    def save(self, entity: CatalogParamEntity) -> CatalogParamEntity:
        obj, _ = CatalogParam.objects.update_or_create(
            id=entity.id,
            defaults={
                "param_type": entity.param_type,
                "code": entity.code,
                "name": entity.name,
                "concesionaria": entity.concesionaria,
            },
        )
        return self._to_entity(obj)

    def delete(self, id: UUID) -> None:
        CatalogParam.objects.filter(id=id).update(deleted_at=datetime.now(timezone.utc))

    @staticmethod
    def _to_entity(m: CatalogParam) -> CatalogParamEntity:
        return CatalogParamEntity(
            id=m.id, param_type=m.param_type, code=m.code,
            name=m.name, concesionaria=m.concesionaria,
            created_at=m.created_at, updated_at=m.updated_at, deleted_at=m.deleted_at,
        )


class DjangoSparePartRepository(ISparePartRepository):
    def find_by_id(self, id: UUID) -> Optional[SparePartEntity]:
        try:
            return self._to_entity(SparePart.objects.get(id=id, deleted_at__isnull=True))
        except SparePart.DoesNotExist:
            return None

    def find_all(self) -> List[SparePartEntity]:
        return [self._to_entity(p) for p in SparePart.objects.filter(deleted_at__isnull=True)]

    def find_by_concesionaria(self, concesionaria: str) -> List[SparePartEntity]:
        return [
            self._to_entity(p)
            for p in SparePart.objects.filter(concesionaria=concesionaria, deleted_at__isnull=True)
        ]

    def find_by_catalog_code(self, catalog_code: str, concesionaria: str) -> Optional[SparePartEntity]:
        try:
            return self._to_entity(
                SparePart.objects.get(catalog_code=catalog_code, concesionaria=concesionaria, deleted_at__isnull=True)
            )
        except SparePart.DoesNotExist:
            return None

    def exists_by_code(self, catalog_code: str, concesionaria: str) -> bool:
        return SparePart.objects.filter(
            catalog_code=catalog_code, concesionaria=concesionaria, deleted_at__isnull=True
        ).exists()

    def save(self, entity: SparePartEntity) -> SparePartEntity:
        obj, _ = SparePart.objects.update_or_create(
            id=entity.id,
            defaults={
                "catalog_code": entity.catalog_code,
                "name": entity.name,
                "unit_price": entity.unit_price,
                "concesionaria": entity.concesionaria,
            },
        )
        return self._to_entity(obj)

    def delete(self, id: UUID) -> None:
        SparePart.objects.filter(id=id).update(deleted_at=datetime.now(timezone.utc))

    @staticmethod
    def _to_entity(m: SparePart) -> SparePartEntity:
        return SparePartEntity(
            id=m.id, catalog_code=m.catalog_code, name=m.name,
            unit_price=m.unit_price, concesionaria=m.concesionaria,
            created_at=m.created_at, updated_at=m.updated_at, deleted_at=m.deleted_at,
        )
