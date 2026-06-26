from uuid import UUID

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from application.dto.user import CreateUserDTO, UpdateUserDTO, ChangePasswordDTO
from application.use_cases.users.create_user import CreateUserUseCase
from application.use_cases.users.delete_user import DeleteUserUseCase
from application.use_cases.users.get_user import GetUserUseCase
from application.use_cases.users.list_users import ListUsersUseCase
from application.use_cases.users.update_user import UpdateUserUseCase
from domain.exceptions.base import EntityNotFoundException, ValidationException
from infrastructure.persistence.models.user import User
from infrastructure.persistence.repositories.user_repository import DjangoUserRepository
from interfaces.api.permissions.roles import IsJefeTallerOrAbove, IsSuperAdmin
from interfaces.api.serializers.user import (
    ChangePasswordSerializer,
    CreateUserSerializer,
    UpdateUserSerializer,
    UserSerializer,
)


def _get_repository() -> DjangoUserRepository:
    return DjangoUserRepository()


class UserViewSet(ViewSet):
    def get_permissions(self):
        if self.action in ("list", "create", "destroy"):
            return [IsJefeTallerOrAbove()]
        if self.action == "update":
            return [IsJefeTallerOrAbove()]
        return super().get_permissions()

    def list(self, request: Request) -> Response:
        concesionaria = None
        if request.user.role != "SUPER_ADMIN":
            concesionaria = request.user.concesionaria

        use_case = ListUsersUseCase(_get_repository())
        users = use_case.execute(concesionaria=concesionaria)
        return Response(UserSerializer(users, many=True).data)

    def create(self, request: Request) -> Response:
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # JefeTaller can only create users in their own concesionaria
        if (
            request.user.role != "SUPER_ADMIN"
            and serializer.validated_data["concesionaria"] != request.user.concesionaria
        ):
            return Response(
                {"detail": "You can only create users in your own concesionaria."},
                status=status.HTTP_403_FORBIDDEN,
            )

        dto = CreateUserDTO(**serializer.validated_data)
        try:
            use_case = CreateUserUseCase(_get_repository())
            user = use_case.execute(dto)
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        except ValidationException as e:
            return Response({"detail": e.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request: Request, pk: str) -> Response:
        try:
            use_case = GetUserUseCase(_get_repository())
            user = use_case.execute(UUID(pk))
            return Response(UserSerializer(user).data)
        except EntityNotFoundException as e:
            return Response({"detail": e.message}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request: Request, pk: str) -> Response:
        serializer = UpdateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        dto = UpdateUserDTO(id=UUID(pk), **serializer.validated_data)
        try:
            use_case = UpdateUserUseCase(_get_repository())
            user = use_case.execute(dto)
            return Response(UserSerializer(user).data)
        except EntityNotFoundException as e:
            return Response({"detail": e.message}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request: Request, pk: str) -> Response:
        if str(request.user.id) == pk:
            return Response(
                {"detail": "You cannot delete your own account."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            use_case = DeleteUserUseCase(_get_repository())
            use_case.execute(UUID(pk))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except EntityNotFoundException as e:
            return Response({"detail": e.message}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=["get"], url_path="me")
    def me(self, request: Request) -> Response:
        use_case = GetUserUseCase(_get_repository())
        user = use_case.execute(request.user.id)
        return Response(UserSerializer(user).data)

    @action(detail=True, methods=["post"], url_path="change-password")
    def change_password(self, request: Request, pk: str) -> Response:
        if str(request.user.id) != pk and request.user.role != "SUPER_ADMIN":
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user_model = User.objects.get(id=pk)
            if not user_model.check_password(serializer.validated_data["current_password"]):
                return Response(
                    {"detail": "Current password is incorrect."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user_model.set_password(serializer.validated_data["new_password"])
            user_model.save(update_fields=["password"])
            return Response({"detail": "Password updated successfully."})
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
