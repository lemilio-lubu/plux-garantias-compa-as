from django.conf import settings
from django.db import models

from infrastructure.persistence.models.user import UserRole
from .base import BaseModel
from .srg import Srg


class SrgPart(BaseModel):
    srg = models.ForeignKey(Srg, on_delete=models.CASCADE, related_name="parts")
    catalog_code = models.CharField(max_length=20)
    name_es = models.CharField(max_length=200)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    part_origin = models.CharField(max_length=50)
    invoice_number = models.CharField(max_length=50)

    class Meta:
        db_table = "srg_parts"
        ordering = ["created_at"]

    def __str__(self) -> str:
        return f"{self.catalog_code} — {self.name_es} (x{self.quantity})"


class SrgEventType(models.TextChoices):
    PART_REQUESTED = "PART_REQUESTED", "Repuesto solicitado"
    RECEPTION_REGISTERED = "RECEPTION_REGISTERED", "Recepción en bodega"
    WORK_REGISTERED = "WORK_REGISTERED", "Repuesto instalado"
    CORE_RETURN_DECLARED = "CORE_RETURN_DECLARED", "Devolución de core declarada"
    RETURN_CONFIRMED = "RETURN_CONFIRMED", "Devolución confirmada en bodega"
    STATUS_CHANGED = "STATUS_CHANGED", "Cambio de estado"


class SrgEvent(BaseModel):
    """Append-only ledger. Doubles as the part quantity ledger (received / used /
    returned are summed from events) and the SRG activity timeline."""

    srg = models.ForeignKey(Srg, on_delete=models.CASCADE, related_name="events")
    srg_part = models.ForeignKey(
        SrgPart, on_delete=models.CASCADE, null=True, blank=True, related_name="events"
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="srg_events",
    )
    actor_role = models.CharField(max_length=20, choices=UserRole.choices, blank=True)
    event_type = models.CharField(max_length=30, choices=SrgEventType.choices)
    quantity = models.PositiveSmallIntegerField(null=True, blank=True)
    state_from = models.CharField(max_length=15, blank=True)
    state_to = models.CharField(max_length=15, blank=True)
    note = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=100, blank=True, default="")

    class Meta:
        db_table = "srg_events"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["srg", "created_at"]),
            models.Index(fields=["srg_part", "event_type"]),
        ]

    def __str__(self) -> str:
        return f"{self.event_type} · OT {self.srg_id} (x{self.quantity})"


class CampaignBody(BaseModel):
    srg = models.OneToOneField(Srg, on_delete=models.CASCADE, related_name="campaign_body")
    update_name = models.CharField(max_length=200)
    image_link = models.URLField(max_length=500)
    modified_by = models.CharField(max_length=150, blank=True)

    class Meta:
        db_table = "campaign_bodies"

    def __str__(self) -> str:
        return f"Campaign body for OT {self.srg.ot}"
