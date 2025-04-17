from rest_framework import serializers
from .models import Branch


class BranchSerializer(serializers.ModelSerializer):
    """
    Serializer for Branch model
    """
    bd_count = serializers.SerializerMethodField()
    active_bd_count = serializers.SerializerMethodField()
    full_address = serializers.SerializerMethodField()
    
    class Meta:
        model = Branch
        fields = [
            'id', 'name', 'code', 'address_line1', 'address_line2', 'city', 
            'state', 'postal_code', 'country', 'phone', 'email', 'is_active',
            'manager_name', 'manager_email', 'manager_phone', 'created_at', 
            'updated_at', 'bd_count', 'active_bd_count', 'full_address'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'bd_count', 'active_bd_count', 'full_address']
    
    def get_bd_count(self, obj):
        """
        Get the number of BDs associated with this branch
        """
        return obj.get_bd_count()
    
    def get_active_bd_count(self, obj):
        """
        Get the number of active BDs associated with this branch
        """
        return obj.get_active_bd_count()
    
    def get_full_address(self, obj):
        """
        Get the full address as a formatted string
        """
        return obj.get_full_address()
    
    def validate_code(self, value):
        """
        Validate that the branch code is uppercase and alphanumeric
        """
        if not value.isalnum():
            raise serializers.ValidationError("Branch code must be alphanumeric")
        
        return value.upper()


class BranchListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for listing branches
    """
    class Meta:
        model = Branch
        fields = ['id', 'name', 'code', 'city', 'state', 'is_active', 'manager_name']
