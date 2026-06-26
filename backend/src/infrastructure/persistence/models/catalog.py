from django.db import models

from infrastructure.persistence.models.user import Concesionaria
from .base import BaseModel


class CatalogParamType(models.TextChoices):
    VEHICLE_MODEL = "VEHICLE_MODEL", "Vehicle Model"
    COLOR = "COLOR", "Color"
    WARRANTY_TYPE = "WARRANTY_TYPE", "Warranty Type"
    CAMPAIGN_CODE = "CAMPAIGN_CODE", "Campaign Code"


class CatalogParam(BaseModel):
    param_type = models.CharField(max_length=20, choices=CatalogParamType.choices)
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=200)
    concesionaria = models.CharField(max_length=20, choices=Concesionaria.choices)

    class Meta:
        db_table = "catalog_params"
        unique_together = [("param_type", "code", "concesionaria")]
        ordering = ["param_type", "name"]

    def __str__(self) -> str:
        return f"[{self.param_type}] {self.code} — {self.name}"


class SparePart(BaseModel):
    catalog_code = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    concesionaria = models.CharField(max_length=20, choices=Concesionaria.choices)

    class Meta:
        db_table = "spare_parts"
        unique_together = [("catalog_code", "concesionaria")]
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.catalog_code} — {self.name}"
