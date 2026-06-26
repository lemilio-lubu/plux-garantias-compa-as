from dataclasses import dataclass, field
from typing import Optional

from .base import BaseEntity


@dataclass
class UserEntity(BaseEntity):
    email: str = ""
    first_name: str = ""
    last_name: str = ""
    role: str = ""
    concesionaria: str = ""
    is_active: bool = True
    password_hash: Optional[str] = None

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def can_manage_concesionaria(self, concesionaria: str) -> bool:
        """SuperAdmin manages all; JefeTaller only their own."""
        if self.role == "SUPER_ADMIN":
            return True
        if self.role == "JEFE_TALLER":
            return self.concesionaria == concesionaria
        return False
