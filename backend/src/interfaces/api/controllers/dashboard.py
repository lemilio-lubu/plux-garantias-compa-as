from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers

from application.use_cases.srg.get_dashboard import GetDashboardUseCase
from infrastructure.persistence.models.user import UserRole
from infrastructure.persistence.repositories.srg_repository import DjangoSrgRepository
from interfaces.api.permissions.roles import IsJefeTallerOrAbove


class StatusCountSerializer(serializers.Serializer):
    status = serializers.CharField()
    count = serializers.IntegerField()


class TypeStatusCountSerializer(serializers.Serializer):
    srg_type = serializers.CharField()
    status = serializers.CharField()
    count = serializers.IntegerField()


class DashboardSerializer(serializers.Serializer):
    concesionaria = serializers.CharField()
    total = serializers.IntegerField()
    by_status = StatusCountSerializer(many=True)
    by_type = serializers.DictField(child=serializers.IntegerField())
    breakdown = TypeStatusCountSerializer(many=True)


class DashboardView(APIView):
    permission_classes = [IsJefeTallerOrAbove]

    def get(self, request: Request) -> Response:
        concesionaria = (
            request.query_params.get("concesionaria")
            if request.user.role == UserRole.SUPER_ADMIN
            else request.user.concesionaria
        )
        stats = GetDashboardUseCase(DjangoSrgRepository()).execute(concesionaria)
        return Response(DashboardSerializer(stats).data)
