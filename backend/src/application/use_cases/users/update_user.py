from application.dto.user import UpdateUserDTO
from application.ports.repositories.user_repository import IUserRepository
from domain.entities.user import UserEntity
from domain.exceptions.base import EntityNotFoundException


class UpdateUserUseCase:
    def __init__(self, repository: IUserRepository) -> None:
        self._repository = repository

    def execute(self, dto: UpdateUserDTO) -> UserEntity:
        user = self._repository.find_by_id(dto.id)
        if user is None:
            raise EntityNotFoundException("User", str(dto.id))

        if dto.first_name is not None:
            user.first_name = dto.first_name.upper()
        if dto.last_name is not None:
            user.last_name = dto.last_name.upper()
        if dto.role is not None:
            user.role = dto.role
        if dto.concesionaria is not None:
            user.concesionaria = dto.concesionaria
        if dto.is_active is not None:
            user.is_active = dto.is_active

        return self._repository.save(user)
