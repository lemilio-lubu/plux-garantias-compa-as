from abc import abstractmethod
from typing import List, Optional

from .base import IRepository
from domain.entities.user import UserEntity


class IUserRepository(IRepository[UserEntity]):
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[UserEntity]: ...

    @abstractmethod
    def find_by_concesionaria(self, concesionaria: str) -> List[UserEntity]: ...

    @abstractmethod
    def exists_by_email(self, email: str) -> bool: ...
