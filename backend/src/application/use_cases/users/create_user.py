from application.dto.user import CreateUserDTO
from application.ports.repositories.user_repository import IUserRepository
from domain.entities.user import UserEntity
from domain.exceptions.base import ValidationException


class CreateUserUseCase:
    def __init__(self, repository: IUserRepository) -> None:
        self._repository = repository

    def execute(self, dto: CreateUserDTO) -> UserEntity:
        if self._repository.exists_by_email(dto.email):
            raise ValidationException(f"Email {dto.email} is already registered")

        entity = UserEntity(
            email=dto.email.upper(),
            first_name=dto.first_name.upper(),
            last_name=dto.last_name.upper(),
            role=dto.role,
            concesionaria=dto.concesionaria,
            is_active=True,
        )
        return self._repository.save(entity, password=dto.password)
