from rest_framework import serializers
from .models import QS

class QSSerializer(serializers.ModelSerializer):
    """
    Serializer for quantity surveyor information
    """
    class Meta:
        model = QS
        fields = [
            'id', 'name', 'company', 'email', 'phone', 'created_at', 
            'updated_at', 'address', 'license_number'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class QSListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for quantity surveyor list view
    """
    class Meta:
        model = QS
        fields = ['id', 'name', 'company', 'email', 'phone']
        read_only_fields = ['id']
