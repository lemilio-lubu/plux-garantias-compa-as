from rest_framework import serializers

from domain.value_objects.srg_event import SrgEventType


class AddSrgPartSerializer(serializers.Serializer):
    catalog_code = serializers.CharField(max_length=20)
    name_es = serializers.CharField(max_length=200)
    quantity = serializers.IntegerField(min_value=1)
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    part_origin = serializers.CharField(max_length=50)
    invoice_number = serializers.CharField(max_length=50)


class SrgPartSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    catalog_code = serializers.CharField(read_only=True)
    name_es = serializers.CharField(read_only=True)
    quantity = serializers.IntegerField(read_only=True)
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    part_origin = serializers.CharField(read_only=True)
    invoice_number = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)


class PartLedgerSerializer(serializers.Serializer):
    """Reads a {part, ledger} dict produced by GetSrgPartsLedgerUseCase."""

    id = serializers.UUIDField(source="part.id")
    catalog_code = serializers.CharField(source="part.catalog_code")
    name_es = serializers.CharField(source="part.name_es")
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2, source="part.unit_price")
    part_origin = serializers.CharField(source="part.part_origin")
    invoice_number = serializers.CharField(source="part.invoice_number")
    created_at = serializers.DateTimeField(source="part.created_at")

    requested = serializers.IntegerField(source="ledger.requested")
    received = serializers.IntegerField(source="ledger.received")
    used = serializers.IntegerField(source="ledger.used")
    returned_declared = serializers.IntegerField(source="ledger.returned_declared")
    returned_confirmed = serializers.IntegerField(source="ledger.returned_confirmed")
    pending_reception = serializers.IntegerField(source="ledger.pending_reception")
    pending_return = serializers.IntegerField(source="ledger.pending_return")
    reception_state = serializers.CharField(source="ledger.reception_state")
    return_state = serializers.CharField(source="ledger.return_state")
    closed = serializers.BooleanField(source="ledger.closed")


class RegisterPartMovementSerializer(serializers.Serializer):
    MOVEMENT_CHOICES = [
        SrgEventType.RECEPTION_REGISTERED.value,
        SrgEventType.WORK_REGISTERED.value,
        SrgEventType.CORE_RETURN_DECLARED.value,
        SrgEventType.RETURN_CONFIRMED.value,
    ]
    event_type = serializers.ChoiceField(choices=MOVEMENT_CHOICES)
    quantity = serializers.IntegerField(min_value=1)
    note = serializers.CharField(max_length=255, required=False, allow_blank=True, default="")


class SrgEventSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    srg_id = serializers.UUIDField(read_only=True)
    srg_part_id = serializers.UUIDField(read_only=True, allow_null=True)
    actor_id = serializers.UUIDField(read_only=True, allow_null=True)
    actor_role = serializers.CharField(read_only=True)
    actor_label = serializers.CharField(read_only=True)
    part_label = serializers.CharField(read_only=True)
    event_type = serializers.CharField(read_only=True)
    quantity = serializers.IntegerField(read_only=True, allow_null=True)
    state_from = serializers.CharField(read_only=True)
    state_to = serializers.CharField(read_only=True)
    note = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)


class TransitionSrgStatusSerializer(serializers.Serializer):
    new_status = serializers.CharField(max_length=15)
    fecha_aprobacion = serializers.DateField(required=False, allow_null=True)

    def validate_new_status(self, value: str) -> str:
        from domain.value_objects.srg_status import SrgStatus
        try:
            SrgStatus(value.upper())
        except ValueError:
            raise serializers.ValidationError(f"Invalid status: {value}")
        return value.upper()


class UpsertCampaignBodySerializer(serializers.Serializer):
    update_name = serializers.CharField(max_length=200)
    image_link = serializers.URLField(max_length=500)


class CampaignBodySerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    srg_id = serializers.UUIDField(read_only=True)
    update_name = serializers.CharField(read_only=True)
    image_link = serializers.URLField(read_only=True)
    modified_by = serializers.CharField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
