from uuid import UUID

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from application.dto.srg_body import (
    AddSrgPartDTO,
    RegisterPartMovementDTO,
    TransitionSrgStatusDTO,
    UpsertCampaignBodyDTO,
)
from application.use_cases.srg.add_srg_part import AddSrgPartUseCase
from application.use_cases.srg.get_srg_parts_ledger import GetSrgPartsLedgerUseCase
from application.use_cases.srg.list_srg_events import ListSrgEventsUseCase
from application.use_cases.srg.manage_campaign_body import (
    GetCampaignBodyUseCase,
    UpsertCampaignBodyUseCase,
)
from application.use_cases.srg.register_part_movement import RegisterPartMovementUseCase
from application.use_cases.srg.transition_status import TransitionSrgStatusUseCase
from domain.exceptions.base import (
    BusinessRuleViolationException,
    EntityNotFoundException,
)
from domain.value_objects.srg_event import SrgEventType
from infrastructure.persistence.models.user import UserRole
from infrastructure.persistence.repositories.srg_body_repository import (
    DjangoCampaignBodyRepository,
    DjangoSrgEventRepository,
    DjangoSrgPartRepository,
)
from infrastructure.persistence.repositories.srg_repository import DjangoSrgRepository
from interfaces.api.serializers.srg_body import (
    AddSrgPartSerializer,
    CampaignBodySerializer,
    PartLedgerSerializer,
    RegisterPartMovementSerializer,
    SrgEventSerializer,
    SrgPartSerializer,
    TransitionSrgStatusSerializer,
    UpsertCampaignBodySerializer,
)

# Which role is allowed to perform each part movement.
BODEGA_MOVEMENTS = {
    SrgEventType.RECEPTION_REGISTERED.value,
    SrgEventType.RETURN_CONFIRMED.value,
}
ASESOR_MOVEMENTS = {
    SrgEventType.WORK_REGISTERED.value,
    SrgEventType.CORE_RETURN_DECLARED.value,
}
MANAGERS = {UserRole.JEFE_TALLER, UserRole.SUPER_ADMIN}


def _srg_repo():
    return DjangoSrgRepository()


def _part_repo():
    return DjangoSrgPartRepository()


def _event_repo():
    return DjangoSrgEventRepository()


def _campaign_repo():
    return DjangoCampaignBodyRepository()


class SrgTransitionView(APIView):
    def post(self, request: Request, srg_id: str) -> Response:
        serializer = TransitionSrgStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dto = TransitionSrgStatusDTO(
            srg_id=UUID(srg_id),
            new_status=serializer.validated_data["new_status"],
            fecha_aprobacion=str(serializer.validated_data["fecha_aprobacion"])
            if serializer.validated_data.get("fecha_aprobacion")
            else None,
        )
        try:
            from interfaces.api.serializers.srg import SrgSerializer
            srg = TransitionSrgStatusUseCase(_srg_repo(), _event_repo()).execute(
                dto, actor_id=request.user.id, actor_role=request.user.role
            )
            return Response(SrgSerializer(srg).data)
        except (EntityNotFoundException, BusinessRuleViolationException) as e:
            code = status.HTTP_404_NOT_FOUND if "not found" in str(e).lower() else status.HTTP_400_BAD_REQUEST
            return Response({"detail": e.message}, status=code)


class SrgPartsView(APIView):
    def get(self, request: Request, srg_id: str) -> Response:
        rows = GetSrgPartsLedgerUseCase(_part_repo(), _event_repo()).execute(UUID(srg_id))
        return Response(PartLedgerSerializer(rows, many=True).data)

    def post(self, request: Request, srg_id: str) -> Response:
        if request.user.role not in ({UserRole.ASESOR} | MANAGERS):
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = AddSrgPartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dto = AddSrgPartDTO(srg_id=UUID(srg_id), **serializer.validated_data)
        try:
            part = AddSrgPartUseCase(_srg_repo(), _part_repo(), _event_repo()).execute(
                dto, actor_id=request.user.id, actor_role=request.user.role
            )
            return Response(SrgPartSerializer(part).data, status=status.HTTP_201_CREATED)
        except (EntityNotFoundException, BusinessRuleViolationException) as e:
            code = status.HTTP_404_NOT_FOUND if "not found" in str(e).lower() else status.HTTP_400_BAD_REQUEST
            return Response({"detail": e.message}, status=code)


class SrgPartMovementView(APIView):
    def post(self, request: Request, srg_id: str, part_id: str) -> Response:
        serializer = RegisterPartMovementSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        event_type = serializer.validated_data["event_type"]
        role = request.user.role

        # Bodeguero registers receptions and confirms returns; asesor registers
        # installs and declares core returns. Managers may do either.
        allowed = role in MANAGERS
        if event_type in BODEGA_MOVEMENTS and role == UserRole.BODEGUERO:
            allowed = True
        if event_type in ASESOR_MOVEMENTS and role == UserRole.ASESOR:
            allowed = True
        if not allowed:
            return Response(status=status.HTTP_403_FORBIDDEN)

        dto = RegisterPartMovementDTO(
            srg_id=UUID(srg_id),
            part_id=UUID(part_id),
            event_type=event_type,
            quantity=serializer.validated_data["quantity"],
            actor_id=request.user.id,
            actor_role=role,
            note=serializer.validated_data.get("note", ""),
        )
        try:
            event = RegisterPartMovementUseCase(_part_repo(), _event_repo()).execute(dto)
            return Response(SrgEventSerializer(event).data, status=status.HTTP_201_CREATED)
        except EntityNotFoundException as e:
            return Response({"detail": e.message}, status=status.HTTP_404_NOT_FOUND)
        except BusinessRuleViolationException as e:
            return Response({"detail": e.message}, status=status.HTTP_400_BAD_REQUEST)


class SrgEventsView(APIView):
    def get(self, request: Request, srg_id: str) -> Response:
        events = ListSrgEventsUseCase(_event_repo()).execute(srg_id=UUID(srg_id))
        return Response(SrgEventSerializer(events, many=True).data)


class GlobalEventsView(APIView):
    def get(self, request: Request) -> Response:
        if request.user.role not in (MANAGERS | {UserRole.AUDITOR}):
            return Response(status=status.HTTP_403_FORBIDDEN)
        concesionaria = (
            request.query_params.get("concesionaria")
            if request.user.role == UserRole.SUPER_ADMIN
            else request.user.concesionaria
        )
        events = ListSrgEventsUseCase(_event_repo()).execute(
            concesionaria=concesionaria,
            event_type=request.query_params.get("event_type"),
        )
        return Response(SrgEventSerializer(events, many=True).data)


class SrgCampaignBodyView(APIView):
    def _check_not_bodeguero(self, request: Request) -> bool:
        return request.user.role != UserRole.BODEGUERO

    def get(self, request: Request, srg_id: str) -> Response:
        if not self._check_not_bodeguero(request):
            return Response(status=status.HTTP_403_FORBIDDEN)
        body = GetCampaignBodyUseCase(_campaign_repo()).execute(UUID(srg_id))
        if body is None:
            return Response({"detail": "Campaign body not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(CampaignBodySerializer(body).data)

    def post(self, request: Request, srg_id: str) -> Response:
        if not self._check_not_bodeguero(request):
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = UpsertCampaignBodySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dto = UpsertCampaignBodyDTO(
            srg_id=UUID(srg_id),
            update_name=serializer.validated_data["update_name"],
            image_link=serializer.validated_data["image_link"],
            modified_by=request.user.email,
        )
        try:
            body = UpsertCampaignBodyUseCase(_srg_repo(), _campaign_repo()).execute(dto)
            return Response(CampaignBodySerializer(body).data, status=status.HTTP_201_CREATED)
        except (EntityNotFoundException, BusinessRuleViolationException) as e:
            code = status.HTTP_404_NOT_FOUND if "not found" in str(e).lower() else status.HTTP_400_BAD_REQUEST
            return Response({"detail": e.message}, status=code)
