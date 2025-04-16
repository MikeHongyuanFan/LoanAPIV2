from rest_framework import serializers
from .models import Broker

class BrokerSerializer(serializers.ModelSerializer):
    """
    Serializer for broker information
    """
    class Meta:
        model = Broker
        fields = [
            'id', 'name', 'company', 'email', 'phone', 'created_at', 
            'updated_at', 'address', 'license_number', 'commission_rate'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class BrokerListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for broker list view
    """
    class Meta:
        model = Broker
        fields = ['id', 'name', 'company', 'email', 'phone']
        read_only_fields = ['id']
