from typing import List, Optional

from application.ports.repositories.user_repository import IUserRepository
from domain.entities.user import UserEntity


class ListUsersUseCase:
    def __init__(self, repository: IUserRepository) -> None:
        self._repository = repository

    def execute(self, concesionaria: Optional[str] = None) -> List[UserEntity]:
        if concesionaria:
            return self._repository.find_by_concesionaria(concesionaria)
        return self._repository.find_all()
