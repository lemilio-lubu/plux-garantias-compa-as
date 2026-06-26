import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def authenticated_client(api_client: APIClient, db) -> APIClient:
    from infrastructure.persistence.models import User, UserRole

    user = User.objects.create_user(
        email="test@plux.com",
        password="TestPass123!",
        first_name="Test",
        last_name="User",
        role=UserRole.ASESOR,
        concesionaria="SURMOTOR",
    )
    api_client.force_authenticate(user=user)
    return api_client
