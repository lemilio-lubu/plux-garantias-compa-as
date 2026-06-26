from typing import List, Optional
from uuid import UUID
from datetime import datetime, timezone

from application.ports.repositories.user_repository import IUserRepository
from domain.entities.user import UserEntity
from infrastructure.persistence.models.user import User


class DjangoUserRepository(IUserRepository):
    def find_by_id(self, id: UUID) -> Optional[UserEntity]:
        try:
            model = User.objects.get(id=id, deleted_at__isnull=True)
            return self._to_entity(model)
        except User.DoesNotExist:
            return None

    def find_all(self) -> List[UserEntity]:
        return [
            self._to_entity(u)
            for u in User.objects.filter(deleted_at__isnull=True).order_by("first_name")
        ]

    def find_by_email(self, email: str) -> Optional[UserEntity]:
        try:
            model = User.objects.get(email=email, deleted_at__isnull=True)
            return self._to_entity(model)
        except User.DoesNotExist:
            return None

    def find_by_concesionaria(self, concesionaria: str) -> List[UserEntity]:
        return [
            self._to_entity(u)
            for u in User.objects.filter(
                concesionaria=concesionaria, deleted_at__isnull=True
            ).order_by("first_name")
        ]

    def exists_by_email(self, email: str) -> bool:
        return User.objects.filter(email=email, deleted_at__isnull=True).exists()

    def save(self, entity: UserEntity, password: Optional[str] = None) -> UserEntity:
        defaults = {
            "first_name": entity.first_name,
            "last_name": entity.last_name,
            "role": entity.role,
            "concesionaria": entity.concesionaria,
            "is_active": entity.is_active,
        }
        model, created = User.objects.update_or_create(id=entity.id, defaults=defaults)
        if created and password:
            model.set_password(password)
            model.email = entity.email
            model.save(update_fields=["email", "password"])
        return self._to_entity(model)

    def delete(self, id: UUID) -> None:
        User.objects.filter(id=id).update(deleted_at=datetime.now(timezone.utc))

    @staticmethod
    def _to_entity(model: User) -> UserEntity:
        return UserEntity(
            id=model.id,
            email=model.email,
            first_name=model.first_name,
            last_name=model.last_name,
            role=model.role,
            concesionaria=model.concesionaria,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
            deleted_at=model.deleted_at,
        )
