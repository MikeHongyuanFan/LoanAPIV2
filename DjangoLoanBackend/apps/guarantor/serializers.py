from rest_framework import serializers
from .models import Guarantor

class GuarantorSerializer(serializers.ModelSerializer):
    """
    Serializer for guarantor information
    """
    class Meta:
        model = Guarantor
        fields = [
            'id', 'type', 'name', 'borrower', 'application', 'created_at',
            'dob', 'email', 'phone', 'address', 'company_name', 'abn', 'acn'
        ]
        read_only_fields = ['id', 'created_at']
        
    def validate(self, data):
        """
        Validate that appropriate fields are provided based on guarantor type
        """
        guarantor_type = data.get('type')
        
        if guarantor_type == 'INDIVIDUAL':
            if not data.get('dob'):
                raise serializers.ValidationError("Date of birth is required for individual guarantors")
        elif guarantor_type == 'COMPANY':
            if not data.get('company_name'):
                raise serializers.ValidationError("Company name is required for company guarantors")
        
        return data
