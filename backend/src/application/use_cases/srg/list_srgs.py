from typing import List, Optional

from application.dto.srg import SearchSrgDTO
from application.ports.repositories.srg_repository import ISrgRepository
from domain.entities.srg import SrgEntity


class ListSrgsUseCase:
    def __init__(self, repository: ISrgRepository) -> None:
        self._repository = repository

    def execute(self, dto: SearchSrgDTO) -> List[SrgEntity]:
        if dto.ot or dto.vin or dto.sede:
            return self._repository.search(
                concesionaria=dto.concesionaria,
                ot=dto.ot,
                vin=dto.vin,
                sede=dto.sede,
            )
        return self._repository.find_by_concesionaria(dto.concesionaria)
