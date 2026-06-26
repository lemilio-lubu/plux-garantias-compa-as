from uuid import UUID

from application.ports.repositories.user_repository import IUserRepository
from domain.exceptions.base import EntityNotFoundException


class DeleteUserUseCase:
    def __init__(self, repository: IUserRepository) -> None:
        self._repository = repository

    def execute(self, user_id: UUID) -> None:
        user = self._repository.find_by_id(user_id)
        if user is None:
            raise EntityNotFoundException("User", str(user_id))
        self._repository.delete(user_id)
