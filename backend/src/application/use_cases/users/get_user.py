from uuid import UUID

from application.ports.repositories.user_repository import IUserRepository
from domain.entities.user import UserEntity
from domain.exceptions.base import EntityNotFoundException


class GetUserUseCase:
    def __init__(self, repository: IUserRepository) -> None:
        self._repository = repository

    def execute(self, user_id: UUID) -> UserEntity:
        user = self._repository.find_by_id(user_id)
        if user is None:
            raise EntityNotFoundException("User", str(user_id))
        return user
