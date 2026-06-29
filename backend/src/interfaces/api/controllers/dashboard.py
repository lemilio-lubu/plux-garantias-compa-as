from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers

from application.use_cases.srg.get_dashboard import GetDashboardUseCase
from infrastructure.persistence.models.user import UserRole
from infrastructure.persistence.repositories.srg_repository import DjangoSrgRepository


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
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        role = request.user.role

        if role == UserRole.SUPER_ADMIN:
            concesionaria = request.query_params.get("concesionaria") or request.user.concesionaria
        else:
            concesionaria = request.user.concesionaria

        asesor_id = request.user.id if role == UserRole.ASESOR else None

        stats = GetDashboardUseCase(DjangoSrgRepository()).execute(concesionaria, asesor_id=asesor_id)
        return Response(DashboardSerializer(stats).data)
