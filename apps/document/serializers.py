from rest_framework import serializers
from .models import Document

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

class DocumentGenerateSerializer(serializers.Serializer):
    """
    Serializer for document generation
    """
    application_id = serializers.UUIDField(required=True)
    document_type = serializers.ChoiceField(choices=Document.TYPE_CHOICES, required=True)
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
        
        return data
