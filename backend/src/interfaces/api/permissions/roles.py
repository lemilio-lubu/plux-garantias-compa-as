from rest_framework.permissions import BasePermission
from infrastructure.persistence.models.user import UserRole


class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view) -> bool:
        return bool(request.user and request.user.is_authenticated and request.user.role == UserRole.SUPER_ADMIN)


class IsJefeTallerOrAbove(BasePermission):
    def has_permission(self, request, view) -> bool:
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role in (UserRole.SUPER_ADMIN, UserRole.JEFE_TALLER)
        )


class IsAsesorOrAbove(BasePermission):
    def has_permission(self, request, view) -> bool:
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role in (UserRole.SUPER_ADMIN, UserRole.JEFE_TALLER, UserRole.ASESOR)
        )


class IsAuditorOrAbove(BasePermission):
    def has_permission(self, request, view) -> bool:
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role in (UserRole.SUPER_ADMIN, UserRole.JEFE_TALLER, UserRole.AUDITOR)
        )


class IsAuditorOnly(BasePermission):
    def has_permission(self, request, view) -> bool:
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == UserRole.AUDITOR
        )


class IsSameConcesionariaOrAbove(BasePermission):
    """JefeTaller can only access objects from their own concesionaria."""

    def has_object_permission(self, request, view, obj) -> bool:
        if request.user.role == UserRole.SUPER_ADMIN:
            return True
        concesionaria = getattr(obj, "concesionaria", None)
        return concesionaria == request.user.concesionaria
