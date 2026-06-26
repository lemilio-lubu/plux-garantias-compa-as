from typing import List
from uuid import UUID

from application.dto.catalog import CreateSparePartDTO, UpdateSparePartDTO
from application.ports.repositories.catalog_repository import ISparePartRepository
from domain.entities.catalog import SparePartEntity
from domain.exceptions.base import EntityNotFoundException, ValidationException


class CreateSparePartUseCase:
    def __init__(self, repository: ISparePartRepository) -> None:
        self._repository = repository

    def execute(self, dto: CreateSparePartDTO) -> SparePartEntity:
        if self._repository.exists_by_code(dto.catalog_code.upper(), dto.concesionaria):
            raise ValidationException(
                f"Spare part '{dto.catalog_code}' already exists in {dto.concesionaria}"
            )
        entity = SparePartEntity(
            catalog_code=dto.catalog_code.upper(),
            name=dto.name.upper(),
            unit_price=dto.unit_price,
            concesionaria=dto.concesionaria,
        )
        return self._repository.save(entity)


class ListSparePartsUseCase:
    def __init__(self, repository: ISparePartRepository) -> None:
        self._repository = repository

    def execute(self, concesionaria: str) -> List[SparePartEntity]:
        return self._repository.find_by_concesionaria(concesionaria)


class UpdateSparePartUseCase:
    def __init__(self, repository: ISparePartRepository) -> None:
        self._repository = repository

    def execute(self, dto: UpdateSparePartDTO) -> SparePartEntity:
        part = self._repository.find_by_id(dto.id)
        if part is None:
            raise EntityNotFoundException("SparePart", str(dto.id))
        if dto.name is not None:
            part.name = dto.name.upper()
        if dto.unit_price is not None:
            part.unit_price = dto.unit_price
        return self._repository.save(part)


class DeleteSparePartUseCase:
    def __init__(self, repository: ISparePartRepository) -> None:
        self._repository = repository

    def execute(self, part_id: UUID) -> None:
        part = self._repository.find_by_id(part_id)
        if part is None:
            raise EntityNotFoundException("SparePart", str(part_id))
        self._repository.delete(part_id)
