import pytest
from unittest.mock import MagicMock
from uuid import uuid4

from application.dto.user import CreateUserDTO
from application.use_cases.users.create_user import CreateUserUseCase
from domain.entities.user import UserEntity
from domain.exceptions.base import ValidationException


@pytest.fixture
def repository():
    return MagicMock()


@pytest.fixture
def use_case(repository):
    return CreateUserUseCase(repository)


def test_create_user_success(use_case, repository):
    repository.exists_by_email.return_value = False
    expected = UserEntity(id=uuid4(), email="JOHN@EXAMPLE.COM", first_name="JOHN", last_name="DOE", role="ASESOR", concesionaria="SURMOTOR")
    repository.save.return_value = expected

    dto = CreateUserDTO(
        email="john@example.com",
        first_name="john",
        last_name="doe",
        role="ASESOR",
        concesionaria="SURMOTOR",
        password="SecurePass1!",
    )
    result = use_case.execute(dto)

    repository.exists_by_email.assert_called_once_with("john@example.com")
    assert result.role == "ASESOR"
    assert result.concesionaria == "SURMOTOR"


def test_create_user_duplicate_email_raises(use_case, repository):
    repository.exists_by_email.return_value = True

    dto = CreateUserDTO(
        email="existing@example.com",
        first_name="Jane",
        last_name="Doe",
        role="ASESOR",
        concesionaria="SURMOTOR",
        password="SecurePass1!",
    )
    with pytest.raises(ValidationException) as exc:
        use_case.execute(dto)

    assert "already registered" in exc.value.message
    repository.save.assert_not_called()
