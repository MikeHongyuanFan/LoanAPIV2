from rest_framework import serializers
from .models import Valuer

class ValuerSerializer(serializers.ModelSerializer):
    """
    Serializer for valuer information
    """
    class Meta:
        model = Valuer
        fields = [
            'id', 'name', 'company', 'email', 'phone', 'created_at', 
            'updated_at', 'address', 'license_number'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class ValuerListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for valuer list view
    """
    class Meta:
        model = Valuer
        fields = ['id', 'name', 'company', 'email', 'phone']
        read_only_fields = ['id']
