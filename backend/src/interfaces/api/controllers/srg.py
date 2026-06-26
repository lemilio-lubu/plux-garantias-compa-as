from uuid import UUID

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from application.dto.srg import CreateCampaignSrgDTO, CreateWarrantySrgDTO, SearchSrgDTO
from application.use_cases.srg.create_campaign_srg import CreateCampaignSrgUseCase
from application.use_cases.srg.create_warranty_srg import CreateWarrantySrgUseCase
from application.use_cases.srg.get_srg import GetSrgUseCase
from application.use_cases.srg.list_srgs import ListSrgsUseCase
from application.use_cases.srg.update_srg import UpdateSrgDTO, UpdateSrgUseCase
from domain.exceptions.base import BusinessRuleViolationException, EntityNotFoundException
from infrastructure.persistence.models.user import UserRole
from infrastructure.persistence.repositories.srg_repository import DjangoSrgRepository
from interfaces.api.serializers.srg import (
    CreateCampaignSrgSerializer,
    CreateWarrantySrgSerializer,
    SrgSerializer,
    UpdateSrgSerializer,
)


def _repo() -> DjangoSrgRepository:
    return DjangoSrgRepository()


class SrgViewSet(ViewSet):
    def list(self, request: Request) -> Response:
        concesionaria = (
            request.query_params.get("concesionaria")
            if request.user.role == UserRole.SUPER_ADMIN
            else request.user.concesionaria
        )
        dto = SearchSrgDTO(
            concesionaria=concesionaria,
            ot=request.query_params.get("ot"),
            vin=request.query_params.get("vin"),
            sede=request.query_params.get("sede"),
        )
        srgs = ListSrgsUseCase(_repo()).execute(dto)
        return Response(SrgSerializer(srgs, many=True).data)

    def retrieve(self, request: Request, pk: str) -> Response:
        try:
            srg = GetSrgUseCase(_repo()).execute(UUID(pk))
            return Response(SrgSerializer(srg).data)
        except EntityNotFoundException as e:
            return Response({"detail": e.message}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request: Request, pk: str) -> Response:
        serializer = UpdateSrgSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dto = UpdateSrgDTO(id=UUID(pk), **serializer.validated_data)
        try:
            srg = UpdateSrgUseCase(_repo()).execute(dto)
            return Response(SrgSerializer(srg).data)
        except EntityNotFoundException as e:
            return Response({"detail": e.message}, status=status.HTTP_404_NOT_FOUND)
        except BusinessRuleViolationException as e:
            return Response({"detail": e.message}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request: Request, pk: str) -> Response:
        """Soft delete — dar de baja / eliminar."""
        repo = _repo()
        srg = repo.find_by_id(UUID(pk))
        if srg is None:
            return Response({"detail": "SRG not found."}, status=status.HTTP_404_NOT_FOUND)
        repo.delete(UUID(pk))
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create_warranty(self, request: Request) -> Response:
        serializer = CreateWarrantySrgSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dto = CreateWarrantySrgDTO(
            concesionaria=request.user.concesionaria,
            asesor_id=request.user.id,
            **serializer.validated_data,
        )
        try:
            srg = CreateWarrantySrgUseCase(_repo()).execute(dto)
        except BusinessRuleViolationException as e:
            return Response({"detail": e.message}, status=status.HTTP_400_BAD_REQUEST)
        return Response(SrgSerializer(srg).data, status=status.HTTP_201_CREATED)

    def create_campaign(self, request: Request) -> Response:
        serializer = CreateCampaignSrgSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dto = CreateCampaignSrgDTO(
            concesionaria=request.user.concesionaria,
            asesor_id=request.user.id,
            **serializer.validated_data,
        )
        try:
            srg = CreateCampaignSrgUseCase(_repo()).execute(dto)
        except BusinessRuleViolationException as e:
            return Response({"detail": e.message}, status=status.HTTP_400_BAD_REQUEST)
        return Response(SrgSerializer(srg).data, status=status.HTTP_201_CREATED)
