from uuid import UUID

from application.ports.repositories.srg_repository import ISrgRepository
from domain.entities.srg import SrgEntity
from domain.exceptions.base import EntityNotFoundException


class GetSrgUseCase:
    def __init__(self, repository: ISrgRepository) -> None:
        self._repository = repository

    def execute(self, srg_id: UUID) -> SrgEntity:
        srg = self._repository.find_by_id(srg_id)
        if srg is None:
            raise EntityNotFoundException("SRG", str(srg_id))
        return srg
