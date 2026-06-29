from django.conf import settings
from django.db import models

from infrastructure.persistence.models.user import Concesionaria
from .base import BaseModel


class SrgType(models.TextChoices):
    WARRANTY = "WARRANTY", "Garantía"
    CAMPAIGN = "CAMPAIGN", "Campaña"


class SrgStatus(models.TextChoices):
    PROCESO = "PROCESO", "Proceso"
    PENDIENTE = "PENDIENTE", "Pendiente"
    PREAPROBADO = "PREAPROBADO", "Preaprobado"
    APROBADO = "APROBADO", "Aprobado"
    RETORNADO = "RETORNADO", "Retornado"
    NEGADO = "NEGADO", "Negado"


class Srg(BaseModel):
    ot = models.CharField(max_length=20, unique=True, db_index=True)
    srg_type = models.CharField(max_length=10, choices=SrgType.choices)
    status = models.CharField(max_length=15, choices=SrgStatus.choices, default=SrgStatus.PROCESO)
    concesionaria = models.CharField(max_length=20, choices=Concesionaria.choices, db_index=True)
    asesor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="srgs",
    )

    # Common header fields
    vin = models.CharField(max_length=17, db_index=True)
    placa = models.CharField(max_length=10, db_index=True)
    vehicle_model = models.CharField(max_length=50)
    vehicle_color = models.CharField(max_length=50, blank=True)
    vehicle_year = models.PositiveSmallIntegerField()
    km_apertura = models.PositiveIntegerField()
    sede = models.CharField(max_length=20, choices=Concesionaria.choices)

    # Warranty-specific
    nro_garantia = models.CharField(max_length=20, blank=True)
    warranty_type_code = models.CharField(max_length=10, blank=True)
    warranty_type_name = models.CharField(max_length=200, blank=True)

    # Campaign-specific
    campaign_code = models.CharField(max_length=20, blank=True)

    # Status timestamps
    fecha_envio_marca = models.DateTimeField(null=True, blank=True)
    fecha_aprobacion = models.DateField(null=True, blank=True)

    class Meta:
        db_table = "srgs"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["concesionaria", "status"]),
            models.Index(fields=["concesionaria", "srg_type"]),
        ]

    def __str__(self) -> str:
        return f"OT {self.ot} [{self.srg_type}] — {self.status}"
