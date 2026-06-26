from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class CreateUserDTO:
    email: str
    first_name: str
    last_name: str
    role: str
    concesionaria: str
    password: str


@dataclass
class UpdateUserDTO:
    id: UUID
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[str] = None
    concesionaria: Optional[str] = None
    is_active: Optional[bool] = None


@dataclass
class ChangePasswordDTO:
    id: UUID
    current_password: str
    new_password: str
