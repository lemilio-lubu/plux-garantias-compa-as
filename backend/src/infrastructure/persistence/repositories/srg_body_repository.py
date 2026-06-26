from typing import Dict, List, Optional
from uuid import UUID
from datetime import datetime, timezone

from django.db.models import Sum

from application.ports.repositories.srg_body_repository import (
    ICampaignBodyRepository,
    ISrgEventRepository,
    ISrgPartRepository,
)
from domain.entities.campaign_body import CampaignBodyEntity
from domain.entities.srg_event import SrgEventEntity
from domain.entities.srg_part import SrgPartEntity
from domain.value_objects.srg_event import COUNTER_OF
from infrastructure.persistence.models.srg_body import (
    CampaignBody,
    SrgEvent,
    SrgPart,
)


class DjangoSrgPartRepository(ISrgPartRepository):
    def find_by_id(self, id: UUID) -> Optional[SrgPartEntity]:
        try:
            return self._to_entity(SrgPart.objects.get(id=id, deleted_at__isnull=True))
        except SrgPart.DoesNotExist:
            return None

    def find_all(self) -> List[SrgPartEntity]:
        return [self._to_entity(p) for p in SrgPart.objects.filter(deleted_at__isnull=True)]

    def find_by_srg(self, srg_id: UUID) -> List[SrgPartEntity]:
        return [
            self._to_entity(p)
            for p in SrgPart.objects.filter(srg_id=srg_id, deleted_at__isnull=True)
        ]

    def save(self, entity: SrgPartEntity) -> SrgPartEntity:
        obj, _ = SrgPart.objects.update_or_create(
            id=entity.id,
            defaults={
                "srg_id": entity.srg_id,
                "catalog_code": entity.catalog_code,
                "name_es": entity.name_es,
                "quantity": entity.quantity,
                "unit_price": entity.unit_price,
                "part_origin": entity.part_origin,
                "invoice_number": entity.invoice_number,
            },
        )
        return self._to_entity(obj)

    def delete(self, id: UUID) -> None:
        SrgPart.objects.filter(id=id).update(deleted_at=datetime.now(timezone.utc))

    @staticmethod
    def _to_entity(m: SrgPart) -> SrgPartEntity:
        return SrgPartEntity(
            id=m.id, srg_id=m.srg_id,
            catalog_code=m.catalog_code, name_es=m.name_es,
            quantity=m.quantity, unit_price=m.unit_price,
            part_origin=m.part_origin, invoice_number=m.invoice_number,
            created_at=m.created_at, updated_at=m.updated_at, deleted_at=m.deleted_at,
        )


class DjangoSrgEventRepository(ISrgEventRepository):
    def find_by_id(self, id: UUID) -> Optional[SrgEventEntity]:
        try:
            return self._to_entity(
                SrgEvent.objects.select_related("actor", "srg_part").get(id=id)
            )
        except SrgEvent.DoesNotExist:
            return None

    def find_all(self) -> List[SrgEventEntity]:
        return [
            self._to_entity(e)
            for e in SrgEvent.objects.select_related("actor", "srg_part").all()
        ]

    def find_by_srg(self, srg_id: UUID) -> List[SrgEventEntity]:
        return [
            self._to_entity(e)
            for e in SrgEvent.objects.filter(srg_id=srg_id).select_related("actor", "srg_part")
        ]

    def part_counters(self, srg_id: UUID) -> Dict[UUID, Dict[str, int]]:
        rows = (
            SrgEvent.objects.filter(srg_id=srg_id, srg_part__isnull=False)
            .values("srg_part_id", "event_type")
            .annotate(total=Sum("quantity"))
        )
        out: Dict[UUID, Dict[str, int]] = {}
        for r in rows:
            counter = COUNTER_OF.get(r["event_type"])
            if counter is None:
                continue
            out.setdefault(r["srg_part_id"], {})[counter] = r["total"] or 0
        return out

    def search(
        self,
        concesionaria: Optional[str] = None,
        event_type: Optional[str] = None,
    ) -> List[SrgEventEntity]:
        qs = SrgEvent.objects.select_related("actor", "srg_part", "srg")
        if concesionaria:
            qs = qs.filter(srg__concesionaria=concesionaria)
        if event_type:
            qs = qs.filter(event_type=event_type)
        return [self._to_entity(e) for e in qs]

    def save(self, entity: SrgEventEntity) -> SrgEventEntity:
        obj, _ = SrgEvent.objects.update_or_create(
            id=entity.id,
            defaults={
                "srg_id": entity.srg_id,
                "srg_part_id": entity.srg_part_id,
                "actor_id": entity.actor_id,
                "actor_role": entity.actor_role,
                "event_type": entity.event_type,
                "quantity": entity.quantity,
                "state_from": entity.state_from,
                "state_to": entity.state_to,
                "note": entity.note,
            },
        )
        return self._to_entity(SrgEvent.objects.select_related("actor", "srg_part").get(id=obj.id))

    def delete(self, id: UUID) -> None:
        SrgEvent.objects.filter(id=id).delete()

    @staticmethod
    def _to_entity(m: SrgEvent) -> SrgEventEntity:
        actor_label = ""
        if m.actor_id and m.actor:
            actor_label = m.actor.full_name or m.actor.email
        part_label = m.srg_part.catalog_code if m.srg_part_id and m.srg_part else ""
        return SrgEventEntity(
            id=m.id, srg_id=m.srg_id, srg_part_id=m.srg_part_id,
            actor_id=m.actor_id, actor_role=m.actor_role,
            event_type=m.event_type, quantity=m.quantity,
            state_from=m.state_from, state_to=m.state_to, note=m.note,
            actor_label=actor_label, part_label=part_label,
            created_at=m.created_at, updated_at=m.updated_at,
        )


class DjangoCampaignBodyRepository(ICampaignBodyRepository):
    def find_by_id(self, id: UUID) -> Optional[CampaignBodyEntity]:
        try:
            return self._to_entity(CampaignBody.objects.get(id=id))
        except CampaignBody.DoesNotExist:
            return None

    def find_all(self) -> List[CampaignBodyEntity]:
        return [self._to_entity(b) for b in CampaignBody.objects.all()]

    def find_by_srg(self, srg_id: UUID) -> Optional[CampaignBodyEntity]:
        try:
            return self._to_entity(CampaignBody.objects.get(srg_id=srg_id))
        except CampaignBody.DoesNotExist:
            return None

    def save(self, entity: CampaignBodyEntity) -> CampaignBodyEntity:
        obj, _ = CampaignBody.objects.update_or_create(
            id=entity.id,
            defaults={
                "srg_id": entity.srg_id,
                "update_name": entity.update_name,
                "image_link": entity.image_link,
                "modified_by": entity.modified_by,
            },
        )
        return self._to_entity(obj)

    def delete(self, id: UUID) -> None:
        CampaignBody.objects.filter(id=id).delete()

    @staticmethod
    def _to_entity(m: CampaignBody) -> CampaignBodyEntity:
        return CampaignBodyEntity(
            id=m.id, srg_id=m.srg_id,
            update_name=m.update_name, image_link=m.image_link,
            modified_by=m.modified_by,
            created_at=m.created_at, updated_at=m.updated_at,
        )
