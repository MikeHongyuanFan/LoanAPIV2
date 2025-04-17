from rest_framework import serializers
from .models import Document, DocumentTemplate, DocuSignIntegration, DocumentSigningRequest

class DocumentSerializer(serializers.ModelSerializer):
    """
    Serializer for document information
    """
    file_url = serializers.ReadOnlyField()
    
    class Meta:
        model = Document
        fields = [
            'id', 'application', 'type', 'file', 'created_at', 
            'name', 'description', 'is_signed', 'file_url'
        ]
        read_only_fields = ['id', 'created_at', 'file_url']

class DocumentUploadSerializer(serializers.ModelSerializer):
    """
    Serializer for document upload
    """
    class Meta:
        model = Document
        fields = ['application', 'type', 'file', 'name', 'description']
        
    def validate(self, data):
        """
        Validate that the file is provided
        """
        if not data.get('file'):
            raise serializers.ValidationError("File is required")
        return data

class DocumentTemplateSerializer(serializers.ModelSerializer):
    """
    Serializer for document template information
    """
    class Meta:
        model = DocumentTemplate
        fields = [
            'id', 'type', 'recipient_type', 'name', 'description', 
            'template_file', 'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class DocuSignIntegrationSerializer(serializers.ModelSerializer):
    """
    Serializer for DocuSign integration settings
    """
    class Meta:
        model = DocuSignIntegration
        fields = [
            'id', 'api_key', 'api_secret', 'integration_key', 'user_id',
            'account_id', 'base_url', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'api_key': {'write_only': True},
            'api_secret': {'write_only': True},
            'integration_key': {'write_only': True}
        }

class DocumentSigningRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for document signing request information
    """
    class Meta:
        model = DocumentSigningRequest
        fields = [
            'id', 'document', 'recipient_email', 'recipient_name', 'status',
            'docusign_envelope_id', 'created_at', 'updated_at', 'completed_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'completed_at', 'docusign_envelope_id']

class DocumentGenerateSerializer(serializers.Serializer):
    """
    Serializer for document generation
    """
    application_id = serializers.UUIDField(required=True)
    document_type = serializers.ChoiceField(choices=Document.TYPE_CHOICES, required=True)
    recipient_type = serializers.ChoiceField(choices=DocumentTemplate.RECIPIENT_CHOICES, default='CLIENT')
    template_data = serializers.JSONField(required=False)
    
    def validate(self, data):
        """
        Validate that the application exists
        """
        from apps.application.models import Application
        
        application_id = data.get('application_id')
        try:
            Application.objects.get(id=application_id)
        except Application.DoesNotExist:
            raise serializers.ValidationError("Application does not exist")
        
        # Validate that a template exists for the document type and recipient type
        document_type = data.get('document_type')
        recipient_type = data.get('recipient_type')
        
        try:
            DocumentTemplate.objects.get(
                type=document_type,
                recipient_type=recipient_type,
                is_active=True
            )
        except DocumentTemplate.DoesNotExist:
            raise serializers.ValidationError(
                f"No active template found for document type '{document_type}' and recipient type '{recipient_type}'"
            )
        
        return data

class DocumentSendForSigningSerializer(serializers.Serializer):
    """
    Serializer for sending a document for signing
    """
    document_id = serializers.UUIDField(required=True)
    recipient_email = serializers.EmailField(required=True)
    recipient_name = serializers.CharField(required=True)
    
    def validate(self, data):
        """
        Validate that the document exists and is not already signed
        """
        document_id = data.get('document_id')
        try:
            document = Document.objects.get(id=document_id)
            if document.is_signed:
                raise serializers.ValidationError("Document is already signed")
        except Document.DoesNotExist:
            raise serializers.ValidationError("Document does not exist")
        
        # Validate that DocuSign integration is configured
        try:
            DocuSignIntegration.objects.get(is_active=True)
        except DocuSignIntegration.DoesNotExist:
            raise serializers.ValidationError("DocuSign integration is not configured")
        
        return data
