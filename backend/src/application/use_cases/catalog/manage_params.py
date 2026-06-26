from typing import List
from uuid import UUID

from application.dto.catalog import CreateCatalogParamDTO
from application.ports.repositories.catalog_repository import ICatalogParamRepository
from domain.entities.catalog import CatalogParamEntity
from domain.exceptions.base import EntityNotFoundException, ValidationException


class CreateCatalogParamUseCase:
    def __init__(self, repository: ICatalogParamRepository) -> None:
        self._repository = repository

    def execute(self, dto: CreateCatalogParamDTO) -> CatalogParamEntity:
        if self._repository.exists(dto.param_type, dto.code.upper(), dto.concesionaria):
            raise ValidationException(
                f"{dto.param_type} with code '{dto.code}' already exists in {dto.concesionaria}"
            )
        entity = CatalogParamEntity(
            param_type=dto.param_type,
            code=dto.code.upper(),
            name=dto.name.upper(),
            concesionaria=dto.concesionaria,
        )
        return self._repository.save(entity)


class ListCatalogParamsUseCase:
    def __init__(self, repository: ICatalogParamRepository) -> None:
        self._repository = repository

    def execute(self, param_type: str, concesionaria: str) -> List[CatalogParamEntity]:
        return self._repository.find_by_type_and_concesionaria(param_type, concesionaria)


class DeleteCatalogParamUseCase:
    def __init__(self, repository: ICatalogParamRepository) -> None:
        self._repository = repository

    def execute(self, param_id: UUID) -> None:
        param = self._repository.find_by_id(param_id)
        if param is None:
            raise EntityNotFoundException("CatalogParam", str(param_id))
        self._repository.delete(param_id)
