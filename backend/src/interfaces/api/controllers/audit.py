from uuid import UUID

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from application.dto.audit import AuditAttachmentDTO, CreateAuditDTO, UpdateAuditDTO
from application.use_cases.audit.create_audit import CreateAuditUseCase
from application.use_cases.audit.get_audit import GetAuditUseCase
from application.use_cases.audit.list_audits import ListAuditsUseCase
from application.use_cases.audit.update_audit import UpdateAuditUseCase
from domain.exceptions.base import EntityNotFoundException, ValidationException
from infrastructure.persistence.models.user import UserRole
from infrastructure.persistence.repositories.audit_repository import DjangoAuditRepository
from infrastructure.persistence.repositories.srg_repository import DjangoSrgRepository
from interfaces.api.permissions.roles import IsAuditorOnly, IsAuditorOrAbove
from interfaces.api.serializers.audit import (
    AuditSerializer,
    CreateAuditSerializer,
    UpdateAuditSerializer,
)


def _audit_repo() -> DjangoAuditRepository:
    return DjangoAuditRepository()


def _srg_repo() -> DjangoSrgRepository:
    return DjangoSrgRepository()


class AuditViewSet(ViewSet):
    def get_permissions(self):
        if self.action in ("create", "partial_update", "destroy"):
            return [IsAuditorOnly()]
        return [IsAuditorOrAbove()]

    def list(self, request: Request) -> Response:
        concesionaria = (
            request.query_params.get("concesionaria")
            if request.user.role == UserRole.SUPER_ADMIN
            else request.user.concesionaria
        )
        audits = ListAuditsUseCase(_audit_repo()).execute(concesionaria)
        return Response(AuditSerializer(audits, many=True).data)

    def retrieve(self, request: Request, pk: str) -> Response:
        try:
            audit = GetAuditUseCase(_audit_repo()).execute(UUID(pk))
            return Response(AuditSerializer(audit).data)
        except EntityNotFoundException as e:
            return Response({"detail": e.message}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request: Request) -> Response:
        serializer = CreateAuditSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        dto = CreateAuditDTO(
            srg_id=data["srg_id"],
            ot_factura=data["ot_factura"],
            observations=data["observations"],
            auditor_id=request.user.id,
            concesionaria=request.user.concesionaria,
            additional_emails=data.get("additional_emails", []),
            attachments=[
                AuditAttachmentDTO(file_name=a["file_name"], file_url=a["file_url"])
                for a in data.get("attachments", [])
            ],
        )
        try:
            audit = CreateAuditUseCase(_audit_repo(), _srg_repo()).execute(dto)
            return Response(AuditSerializer(audit).data, status=status.HTTP_201_CREATED)
        except EntityNotFoundException as e:
            return Response({"detail": e.message}, status=status.HTTP_404_NOT_FOUND)
        except ValidationException as e:
            return Response({"detail": e.message}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request: Request, pk: str) -> Response:
        serializer = UpdateAuditSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        attachments = None
        if "attachments" in data:
            attachments = [
                AuditAttachmentDTO(file_name=a["file_name"], file_url=a["file_url"])
                for a in data["attachments"]
            ]

        dto = UpdateAuditDTO(
            id=UUID(pk),
            ot_factura=data.get("ot_factura"),
            observations=data.get("observations"),
            additional_emails=data.get("additional_emails"),
            attachments=attachments,
        )
        try:
            audit = UpdateAuditUseCase(_audit_repo()).execute(dto)
            return Response(AuditSerializer(audit).data)
        except EntityNotFoundException as e:
            return Response({"detail": e.message}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request: Request, pk: str) -> Response:
        try:
            repo = _audit_repo()
            audit = repo.find_by_id(UUID(pk))
            if audit is None:
                return Response({"detail": "Audit not found."}, status=status.HTTP_404_NOT_FOUND)
            repo.delete(UUID(pk))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
