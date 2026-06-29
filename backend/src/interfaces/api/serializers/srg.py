from rest_framework import serializers
from infrastructure.persistence.models.user import Concesionaria


class SrgSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    ot = serializers.CharField(read_only=True)
    srg_type = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    concesionaria = serializers.CharField(read_only=True)
    asesor_id = serializers.UUIDField(read_only=True)
    vin = serializers.CharField(read_only=True)
    placa = serializers.CharField(read_only=True)
    vehicle_model = serializers.CharField(read_only=True)
    vehicle_color = serializers.CharField(read_only=True)
    vehicle_year = serializers.IntegerField(read_only=True)
    km_apertura = serializers.IntegerField(read_only=True)
    sede = serializers.CharField(read_only=True)
    nro_garantia = serializers.CharField(read_only=True, allow_null=True)
    warranty_type_code = serializers.CharField(read_only=True, allow_null=True)
    warranty_type_name = serializers.CharField(read_only=True, allow_null=True)
    campaign_code = serializers.CharField(read_only=True, allow_null=True)
    fecha_envio_marca = serializers.DateTimeField(read_only=True, allow_null=True)
    fecha_aprobacion = serializers.DateField(read_only=True, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)


class CreateWarrantySrgSerializer(serializers.Serializer):
    ot = serializers.RegexField(
        r"^[A-Za-z0-9]+$",
        max_length=20,
        error_messages={"invalid": "La OT solo admite letras y números (alfanumérico)."},
    )
    vin = serializers.CharField(max_length=17)
    placa = serializers.CharField(max_length=10)
    vehicle_model = serializers.CharField(max_length=50)
    vehicle_color = serializers.CharField(max_length=50)
    vehicle_year = serializers.IntegerField(min_value=2000, max_value=2100)
    km_apertura = serializers.IntegerField(min_value=0)
    sede = serializers.ChoiceField(choices=Concesionaria.choices)
    nro_garantia = serializers.CharField(max_length=20)
    warranty_type_code = serializers.CharField(max_length=10)
    warranty_type_name = serializers.CharField(max_length=200)


class CreateCampaignSrgSerializer(serializers.Serializer):
    ot = serializers.RegexField(
        r"^[A-Za-z0-9]+$",
        max_length=20,
        error_messages={"invalid": "La OT solo admite letras y números (alfanumérico)."},
    )
    vin = serializers.CharField(max_length=17)
    placa = serializers.CharField(max_length=10)
    vehicle_model = serializers.CharField(max_length=50)
    vehicle_year = serializers.IntegerField(min_value=2000, max_value=2100)
    km_apertura = serializers.IntegerField(min_value=0)
    sede = serializers.ChoiceField(choices=Concesionaria.choices)
    campaign_code = serializers.CharField(max_length=20)


class UpdateSrgSerializer(serializers.Serializer):
    # Common
    vin = serializers.CharField(max_length=17, required=False)
    placa = serializers.CharField(max_length=10, required=False)
    vehicle_model = serializers.CharField(max_length=50, required=False)
    vehicle_color = serializers.CharField(max_length=50, required=False)
    vehicle_year = serializers.IntegerField(min_value=2000, max_value=2100, required=False)
    km_apertura = serializers.IntegerField(min_value=0, required=False)
    sede = serializers.ChoiceField(choices=Concesionaria.choices, required=False)
    # Warranty
    nro_garantia = serializers.CharField(max_length=20, required=False)
    warranty_type_code = serializers.CharField(max_length=10, required=False)
    warranty_type_name = serializers.CharField(max_length=200, required=False)
    # Campaign
    campaign_code = serializers.CharField(max_length=20, required=False)
