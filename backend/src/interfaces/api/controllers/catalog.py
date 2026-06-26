from uuid import UUID

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from application.dto.catalog import CreateCatalogParamDTO, CreateSparePartDTO, UpdateSparePartDTO
from application.use_cases.catalog.manage_params import (
    CreateCatalogParamUseCase,
    DeleteCatalogParamUseCase,
    ListCatalogParamsUseCase,
)
from application.use_cases.catalog.manage_spare_parts import (
    CreateSparePartUseCase,
    DeleteSparePartUseCase,
    ListSparePartsUseCase,
    UpdateSparePartUseCase,
)
from domain.exceptions.base import EntityNotFoundException, ValidationException
from infrastructure.persistence.repositories.catalog_repository import (
    DjangoCatalogParamRepository,
    DjangoSparePartRepository,
)
from interfaces.api.permissions.roles import IsAsesorOrAbove, IsJefeTallerOrAbove
from interfaces.api.serializers.catalog import (
    CatalogParamSerializer,
    CreateCatalogParamSerializer,
    CreateSparePartSerializer,
    SparePartSerializer,
    UpdateSparePartSerializer,
)


class CatalogParamViewSet(ViewSet):
    permission_classes = [IsJefeTallerOrAbove]

    def get_permissions(self):
        # Catalog params are reference data the SRG creation form depends on,
        # so any authenticated user (e.g. ASESOR) may read them. Mutating the
        # catalog stays restricted to Jefe de Taller and above.
        if self.action == "list":
            return [IsAuthenticated()]
        return [IsJefeTallerOrAbove()]

    def list(self, request: Request) -> Response:
        param_type = request.query_params.get("type", "")
        concesionaria = request.query_params.get("concesionaria") or request.user.concesionaria
        repo = DjangoCatalogParamRepository()
        params = ListCatalogParamsUseCase(repo).execute(param_type, concesionaria)
        return Response(CatalogParamSerializer(params, many=True).data)

    def create(self, request: Request) -> Response:
        serializer = CreateCatalogParamSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dto = CreateCatalogParamDTO(**serializer.validated_data)
        try:
            param = CreateCatalogParamUseCase(DjangoCatalogParamRepository()).execute(dto)
            return Response(CatalogParamSerializer(param).data, status=status.HTTP_201_CREATED)
        except ValidationException as e:
            return Response({"detail": e.message}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request: Request, pk: str) -> Response:
        try:
            DeleteCatalogParamUseCase(DjangoCatalogParamRepository()).execute(UUID(pk))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except EntityNotFoundException as e:
            return Response({"detail": e.message}, status=status.HTTP_404_NOT_FOUND)


class SparePartViewSet(ViewSet):
    # Asesores manage the spare-parts catalog of their own dealership with the
    # same capabilities as Jefe de Taller (create / read / update / delete).
    permission_classes = [IsAsesorOrAbove]

    def list(self, request: Request) -> Response:
        concesionaria = request.query_params.get("concesionaria") or request.user.concesionaria
        parts = ListSparePartsUseCase(DjangoSparePartRepository()).execute(concesionaria)
        return Response(SparePartSerializer(parts, many=True).data)

    def create(self, request: Request) -> Response:
        serializer = CreateSparePartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dto = CreateSparePartDTO(**serializer.validated_data)
        try:
            part = CreateSparePartUseCase(DjangoSparePartRepository()).execute(dto)
            return Response(SparePartSerializer(part).data, status=status.HTTP_201_CREATED)
        except ValidationException as e:
            return Response({"detail": e.message}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request: Request, pk: str) -> Response:
        serializer = UpdateSparePartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dto = UpdateSparePartDTO(id=UUID(pk), **serializer.validated_data)
        try:
            part = UpdateSparePartUseCase(DjangoSparePartRepository()).execute(dto)
            return Response(SparePartSerializer(part).data)
        except EntityNotFoundException as e:
            return Response({"detail": e.message}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request: Request, pk: str) -> Response:
        try:
            DeleteSparePartUseCase(DjangoSparePartRepository()).execute(UUID(pk))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except EntityNotFoundException as e:
            return Response({"detail": e.message}, status=status.HTTP_404_NOT_FOUND)
