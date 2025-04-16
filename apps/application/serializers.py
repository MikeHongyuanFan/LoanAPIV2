from rest_framework import serializers
from .models import Application, Note, Repayment, Extension, Fee, Payment
from apps.borrower.serializers import BorrowerSerializer
from apps.broker.serializers import BrokerSerializer
from apps.valuer.serializers import ValuerSerializer
from apps.qs.serializers import QSSerializer
from apps.product.serializers import ProductSerializer

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

class ApplicationSerializer(serializers.ModelSerializer):
    """
    Serializer for loan applications
    """
    class Meta:
        model = Application
        fields = [
            'id', 'borrower', 'broker', 'status', 'loan_amount', 'product',
            'created_at', 'updated_at', 'valuer', 'qs', 'property_address',
            'loan_term_months', 'interest_rate', 'settlement_date', 'expiry_date',
            'loan_purpose', 'property_type', 'property_value', 'reference_number'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'reference_number']

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
    
    class Meta:
        model = Application
        fields = [
            'id', 'borrower', 'broker', 'status', 'loan_amount', 'product',
            'created_at', 'updated_at', 'valuer', 'qs', 'property_address',
            'loan_term_months', 'interest_rate', 'settlement_date', 'expiry_date',
            'loan_purpose', 'property_type', 'property_value', 'reference_number',
            'notes', 'repayments', 'extensions', 'fees', 'payments'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'reference_number']

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
