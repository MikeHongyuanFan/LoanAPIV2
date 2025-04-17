from rest_framework import serializers
from .models import Application, Note, Repayment, Extension, Fee, Payment
from apps.borrower.serializers import BorrowerSerializer
from apps.broker.serializers import BrokerSerializer
from apps.valuer.serializers import ValuerSerializer
from apps.qs.serializers import QSSerializer
from apps.product.serializers import ProductSerializer


class ValuerInfoSerializer(serializers.Serializer):
    """
    Serializer for valuer information stored in the Application model
    """
    company_name = serializers.CharField(max_length=255, required=True)
    contact_name = serializers.CharField(max_length=255, required=True)
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(max_length=20, required=True)


class QSInfoSerializer(serializers.Serializer):
    """
    Serializer for QS information stored in the Application model
    """
    company_name = serializers.CharField(max_length=255, required=True)
    contact_name = serializers.CharField(max_length=255, required=True)
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(max_length=20, required=True)

class FeeSerializer(serializers.ModelSerializer):
    """
    Serializer for fee information
    """
    class Meta:
        model = Fee
        fields = [
            'id', 'application', 'description', 'amount', 'fee_type', 
            'status', 'due_date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for payment information
    """
    class Meta:
        model = Payment
        fields = [
            'id', 'application', 'amount', 'payment_date', 
            'payment_method', 'reference', 'notes', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

class NoteSerializer(serializers.ModelSerializer):
    """
    Serializer for application notes
    """
    class Meta:
        model = Note
        fields = ['id', 'application', 'content', 'has_reminder', 'reminder_date', 'created_by', 'created_at']
        read_only_fields = ['id', 'created_at']

class RepaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for application repayments
    """
    class Meta:
        model = Repayment
        fields = ['id', 'application', 'due_date', 'amount', 'principal_amount', 'interest_amount', 'status', 'paid_date', 'paid_amount']
        read_only_fields = ['id']

class ExtensionSerializer(serializers.ModelSerializer):
    """
    Serializer for loan extensions
    """
    class Meta:
        model = Extension
        fields = ['id', 'application', 'requested_date', 'original_expiry_date', 'new_expiry_date', 'reason', 'status', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def validate(self, data):
        """
        Handle date conversion for expiry dates.
        """
        from django.utils.dateparse import parse_date
        
        # Convert string dates to date objects
        if 'original_expiry_date' in data and isinstance(data['original_expiry_date'], str):
            try:
                data['original_expiry_date'] = parse_date(data['original_expiry_date'])
            except ValueError:
                raise serializers.ValidationError({'original_expiry_date': 'Invalid date format'})
                
        if 'new_expiry_date' in data and isinstance(data['new_expiry_date'], str):
            try:
                data['new_expiry_date'] = parse_date(data['new_expiry_date'])
            except ValueError:
                raise serializers.ValidationError({'new_expiry_date': 'Invalid date format'})
                
        return data

class ApplicationSerializer(serializers.ModelSerializer):
    """
    Serializer for loan applications
    """
    valuer_info = ValuerInfoSerializer(required=False)
    qs_info = QSInfoSerializer(required=False)
    
    class Meta:
        model = Application
        fields = [
            'id', 'borrower', 'broker', 'status', 'stage', 'stage_changed_at',
            'loan_amount', 'product', 'created_at', 'updated_at', 'valuer', 'qs',
            'valuer_info', 'qs_info', 'property_address', 'loan_term_months', 
            'interest_rate', 'settlement_date', 'expiry_date', 'loan_purpose', 
            'property_type', 'property_value', 'reference_number'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'reference_number', 'stage_changed_at']
    
    def validate_valuer_info(self, value):
        """
        Validate valuer_info field
        """
        if value and not isinstance(value, dict):
            raise serializers.ValidationError("valuer_info must be a dictionary")
        
        # If the application is in valuation stage, valuer_info is required
        if self.instance and self.instance.stage == 'VALUATION' and not value:
            raise serializers.ValidationError("valuer_info is required when application is in VALUATION stage")
        
        return value
    
    def validate_qs_info(self, value):
        """
        Validate qs_info field
        """
        if value and not isinstance(value, dict):
            raise serializers.ValidationError("qs_info must be a dictionary")
        
        # If the application is in dual stage, qs_info is required
        if self.instance and self.instance.stage == 'DUAL' and not value:
            raise serializers.ValidationError("qs_info is required when application is in DUAL stage")
        
        return value

class ApplicationDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for loan applications with related entities
    """
    borrower = BorrowerSerializer(read_only=True)
    broker = BrokerSerializer(read_only=True)
    valuer = ValuerSerializer(read_only=True)
    qs = QSSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    notes = NoteSerializer(many=True, read_only=True)
    repayments = RepaymentSerializer(many=True, read_only=True)
    extensions = ExtensionSerializer(many=True, read_only=True)
    fees = FeeSerializer(many=True, read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)
    valuer_info = ValuerInfoSerializer(required=False)
    qs_info = QSInfoSerializer(required=False)
    
    class Meta:
        model = Application
        fields = [
            'id', 'borrower', 'broker', 'status', 'stage', 'stage_changed_at',
            'loan_amount', 'product', 'created_at', 'updated_at', 'valuer', 'qs',
            'valuer_info', 'qs_info', 'property_address', 'loan_term_months', 
            'interest_rate', 'settlement_date', 'expiry_date', 'loan_purpose', 
            'property_type', 'property_value', 'reference_number',
            'notes', 'repayments', 'extensions', 'fees', 'payments'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'reference_number', 'stage_changed_at']

class LoanCalculatorSerializer(serializers.Serializer):
    """
    Serializer for loan calculator functionality
    """
    gross_loan_amount = serializers.DecimalField(max_digits=15, decimal_places=2, required=False)
    net_loan_amount = serializers.DecimalField(max_digits=15, decimal_places=2, required=False)
    establishment_fee = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    valuation_fee = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    legal_fee = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    broker_fee = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    other_fees = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    
    def validate(self, data):
        """
        Validate that either gross_loan_amount or net_loan_amount is provided
        """
        if 'gross_loan_amount' not in data and 'net_loan_amount' not in data:
            raise serializers.ValidationError("Either gross_loan_amount or net_loan_amount must be provided")
        return data
