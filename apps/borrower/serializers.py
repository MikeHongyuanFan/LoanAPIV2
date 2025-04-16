from rest_framework import serializers
from .models import Borrower

class BorrowerSerializer(serializers.ModelSerializer):
    """
    Serializer for borrower information
    """
    class Meta:
        model = Borrower
        fields = [
            'id', 'name', 'dob', 'email', 'phone', 'address', 
            'created_at', 'updated_at', 'company_name', 'abn', 'acn', 'broker'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class BorrowerListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for borrower list view
    """
    class Meta:
        model = Borrower
        fields = ['id', 'name', 'email', 'phone', 'company_name']
        read_only_fields = ['id']
