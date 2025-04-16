from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for loan product information
    """
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'interest_rate', 'created_at', 
            'updated_at', 'min_loan_amount', 'max_loan_amount', 'min_term', 
            'max_term', 'establishment_fee', 'is_active'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class ProductListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for product list view
    """
    class Meta:
        model = Product
        fields = ['id', 'name', 'interest_rate', 'min_loan_amount', 'max_loan_amount', 'is_active']
        read_only_fields = ['id']
