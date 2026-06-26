import pytest
from unittest.mock import MagicMock
from uuid import uuid4

from application.use_cases.users.get_user import GetUserUseCase
from domain.entities.user import UserEntity
from domain.exceptions.base import EntityNotFoundException


@pytest.fixture
def repository():
    return MagicMock()


@pytest.fixture
def use_case(repository):
    return GetUserUseCase(repository)


def test_get_user_found(use_case, repository):
    user_id = uuid4()
    expected = UserEntity(id=user_id, email="test@example.com", first_name="Test", last_name="User", role="ASESOR", concesionaria="SHYRIS")
    repository.find_by_id.return_value = expected

    result = use_case.execute(user_id)

    assert result.id == user_id
    repository.find_by_id.assert_called_once_with(user_id)


def test_get_user_not_found_raises(use_case, repository):
    repository.find_by_id.return_value = None

    with pytest.raises(EntityNotFoundException) as exc:
        use_case.execute(uuid4())

    assert exc.value.code == "NOT_FOUND"
