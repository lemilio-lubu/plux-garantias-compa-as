from rest_framework import serializers
from infrastructure.persistence.models.catalog import CatalogParamType
from infrastructure.persistence.models.user import Concesionaria


class CatalogParamSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    param_type = serializers.CharField(read_only=True)
    code = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    concesionaria = serializers.CharField(read_only=True)


class CreateCatalogParamSerializer(serializers.Serializer):
    param_type = serializers.ChoiceField(choices=CatalogParamType.choices)
    code = serializers.CharField(max_length=50)
    name = serializers.CharField(max_length=200)
    concesionaria = serializers.ChoiceField(choices=Concesionaria.choices)


class SparePartSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    catalog_code = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    concesionaria = serializers.CharField(read_only=True)


class CreateSparePartSerializer(serializers.Serializer):
    catalog_code = serializers.CharField(max_length=20)
    name = serializers.CharField(max_length=200)
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    concesionaria = serializers.ChoiceField(choices=Concesionaria.choices)


class UpdateSparePartSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200, required=False)
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
