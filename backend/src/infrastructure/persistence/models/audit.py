from django.conf import settings
from django.db import models

from infrastructure.persistence.models.srg import Srg
from infrastructure.persistence.models.user import Concesionaria
from .base import BaseModel


class Audit(BaseModel):
    srg = models.OneToOneField(Srg, on_delete=models.PROTECT, related_name="audit")
    ot_factura = models.CharField(max_length=20)
    observations = models.TextField()
    concesionaria = models.CharField(max_length=20, choices=Concesionaria.choices, db_index=True)
    auditor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="audits",
    )
    # PostgreSQL JSON arrays — avoids extra join tables for simple lists
    additional_emails = models.JSONField(default=list, blank=True)
    attachments = models.JSONField(default=list, blank=True)

    class Meta:
        db_table = "audits"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Audit OT {self.srg.ot} — {self.ot_factura}"
