from typing import List, Optional
from uuid import UUID
from datetime import datetime, timezone

from django.db.models import Count, Max

from application.ports.repositories.srg_repository import ISrgRepository
from domain.entities.srg import SrgEntity
from domain.value_objects.srg_status import SrgStatus
from domain.value_objects.srg_type import SrgType
from infrastructure.persistence.models.srg import Srg


class DjangoSrgRepository(ISrgRepository):
    def find_by_id(self, id: UUID) -> Optional[SrgEntity]:
        try:
            return self._to_entity(Srg.objects.get(id=id, deleted_at__isnull=True))
        except Srg.DoesNotExist:
            return None

    def find_all(self) -> List[SrgEntity]:
        return [self._to_entity(s) for s in Srg.objects.filter(deleted_at__isnull=True)]

    def find_by_ot(self, ot: str) -> Optional[SrgEntity]:
        try:
            return self._to_entity(Srg.objects.get(ot=ot, deleted_at__isnull=True))
        except Srg.DoesNotExist:
            return None

    def find_by_concesionaria(self, concesionaria: str) -> List[SrgEntity]:
        return [
            self._to_entity(s)
            for s in Srg.objects.filter(concesionaria=concesionaria, deleted_at__isnull=True)
        ]

    def search(
        self,
        concesionaria: str,
        ot: Optional[str] = None,
        vin: Optional[str] = None,
        sede: Optional[str] = None,
    ) -> List[SrgEntity]:
        qs = Srg.objects.filter(concesionaria=concesionaria, deleted_at__isnull=True)
        if ot:
            qs = qs.filter(ot__icontains=ot)
        if vin:
            qs = qs.filter(vin__icontains=vin)
        if sede:
            qs = qs.filter(sede__icontains=sede)
        return [self._to_entity(s) for s in qs]

    def next_correlativo(self, concesionaria: str, year: int) -> int:
        prefix = str(year)
        result = Srg.objects.filter(
            concesionaria=concesionaria,
            ot__startswith=prefix,
        ).aggregate(max_ot=Max("ot"))
        max_ot = result["max_ot"]
        if max_ot is None:
            return 1
        current = int(max_ot[len(prefix):])
        return current + 1

    def save(self, entity: SrgEntity) -> SrgEntity:
        obj, _ = Srg.objects.update_or_create(
            id=entity.id,
            defaults={
                "ot": entity.ot,
                "srg_type": entity.srg_type,
                "status": entity.status,
                "concesionaria": entity.concesionaria,
                "asesor_id": entity.asesor_id,
                "vin": entity.vin,
                "placa": entity.placa,
                "vehicle_model": entity.vehicle_model,
                "vehicle_color": entity.vehicle_color or "",
                "vehicle_year": entity.vehicle_year,
                "km_apertura": entity.km_apertura,
                "sede": entity.sede,
                "nro_garantia": entity.nro_garantia or "",
                "warranty_type_code": entity.warranty_type_code or "",
                "warranty_type_name": entity.warranty_type_name or "",
                "campaign_code": entity.campaign_code or "",
                "fecha_envio_marca": entity.fecha_envio_marca,
                "fecha_aprobacion": entity.fecha_aprobacion,
            },
        )
        return self._to_entity(obj)

    def delete(self, id: UUID) -> None:
        Srg.objects.filter(id=id).update(deleted_at=datetime.now(timezone.utc))

    def get_dashboard_stats(self, concesionaria: str, asesor_id=None) -> list[dict]:
        qs = Srg.objects.filter(concesionaria=concesionaria, deleted_at__isnull=True)
        if asesor_id is not None:
            qs = qs.filter(asesor_id=asesor_id)
        rows = (
            qs.values("srg_type", "status")
            .annotate(count=Count("id"))
            .order_by("srg_type", "status")
        )
        return [{"srg_type": r["srg_type"], "status": r["status"], "count": r["count"]} for r in rows]

    @staticmethod
    def _to_entity(m: Srg) -> SrgEntity:
        return SrgEntity(
            id=m.id,
            ot=m.ot,
            srg_type=SrgType(m.srg_type),
            status=SrgStatus(m.status),
            concesionaria=m.concesionaria,
            asesor_id=m.asesor_id,
            vin=m.vin,
            placa=m.placa,
            vehicle_model=m.vehicle_model,
            vehicle_color=m.vehicle_color,
            vehicle_year=m.vehicle_year,
            km_apertura=m.km_apertura,
            sede=m.sede,
            nro_garantia=m.nro_garantia or None,
            warranty_type_code=m.warranty_type_code or None,
            warranty_type_name=m.warranty_type_name or None,
            campaign_code=m.campaign_code or None,
            fecha_envio_marca=m.fecha_envio_marca,
            fecha_aprobacion=m.fecha_aprobacion,
            created_at=m.created_at,
            updated_at=m.updated_at,
            deleted_at=m.deleted_at,
        )
