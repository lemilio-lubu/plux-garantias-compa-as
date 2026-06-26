from rest_framework import serializers


class AuditAttachmentSerializer(serializers.Serializer):
    file_name = serializers.CharField(max_length=200)
    file_url = serializers.URLField(max_length=500)


class CreateAuditSerializer(serializers.Serializer):
    srg_id = serializers.UUIDField()
    ot_factura = serializers.CharField(max_length=20)
    observations = serializers.CharField()
    additional_emails = serializers.ListField(
        child=serializers.EmailField(), required=False, default=list
    )
    attachments = AuditAttachmentSerializer(many=True, required=False, default=list)


class UpdateAuditSerializer(serializers.Serializer):
    ot_factura = serializers.CharField(max_length=20, required=False)
    observations = serializers.CharField(required=False)
    additional_emails = serializers.ListField(
        child=serializers.EmailField(), required=False
    )
    attachments = AuditAttachmentSerializer(many=True, required=False)


class AuditSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    srg_id = serializers.UUIDField(read_only=True)
    ot_factura = serializers.CharField(read_only=True)
    observations = serializers.CharField(read_only=True)
    concesionaria = serializers.CharField(read_only=True)
    auditor_id = serializers.UUIDField(read_only=True)
    additional_emails = serializers.ListField(
        child=serializers.EmailField(), read_only=True
    )
    attachments = AuditAttachmentSerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
