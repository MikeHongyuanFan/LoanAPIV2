from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for loan product information
    """
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'min_interest_rate', 'max_interest_rate', 'created_at', 
            'updated_at', 'min_loan_amount', 'max_loan_amount', 'min_term_months', 
            'max_term_months', 'establishment_fee', 'active', 'loan_type'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class ProductListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for product list view
    """
    class Meta:
        model = Product
        fields = ['id', 'name', 'min_interest_rate', 'max_interest_rate', 'min_loan_amount', 'max_loan_amount', 'active']
        read_only_fields = ['id']
