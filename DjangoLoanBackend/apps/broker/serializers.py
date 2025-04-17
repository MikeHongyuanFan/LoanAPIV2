from rest_framework import serializers
from .models import Broker, BrokerCommission, CommissionPayment, CommissionPaymentItem, BrokerTier, BrokerSpecialization
from apps.branch.serializers import BranchListSerializer
from apps.bd.serializers import BDListSerializer


class BrokerTierSerializer(serializers.ModelSerializer):
    """
    Serializer for the BrokerTier model.
    """
    class Meta:
        model = BrokerTier
        fields = ['id', 'name', 'description', 'commission_multiplier', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class BrokerSpecializationSerializer(serializers.ModelSerializer):
    """
    Serializer for the BrokerSpecialization model.
    """
    class Meta:
        model = BrokerSpecialization
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class BrokerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Broker model.
    """
    branch_details = BranchListSerializer(source='branch', read_only=True)
    bd_details = BDListSerializer(source='bd', read_only=True)
    tier_details = BrokerTierSerializer(source='tier', read_only=True)
    specialization_details = BrokerSpecializationSerializer(source='specializations', many=True, read_only=True)
    branch_name = serializers.SerializerMethodField()
    bd_name = serializers.SerializerMethodField()
    tier_name = serializers.SerializerMethodField()
    specialization_names = serializers.SerializerMethodField()
    accreditation_valid = serializers.SerializerMethodField()
    
    class Meta:
        model = Broker
        fields = [
            'id', 'name', 'email', 'phone', 'company', 'address', 'license_number',
            'commission_rate', 'active', 'created_at', 'updated_at',
            'branch', 'branch_name', 'branch_details',
            'bd', 'bd_name', 'bd_details',
            'tier', 'tier_name', 'tier_details',
            'specializations', 'specialization_names', 'specialization_details',
            'years_of_experience', 'accreditation_number', 'accreditation_expiry',
            'profile_image', 'bio', 'website', 'linkedin_profile', 'accreditation_valid'
        ]
        read_only_fields = ['created_at', 'updated_at', 'branch_name', 'bd_name', 'tier_name', 
                           'specialization_names', 'accreditation_valid']
    
    def get_branch_name(self, obj):
        return obj.get_branch_name()
    
    def get_bd_name(self, obj):
        return obj.get_bd_name()
    
    def get_tier_name(self, obj):
        return obj.get_tier_name()
    
    def get_specialization_names(self, obj):
        return obj.get_specialization_names()
    
    def get_accreditation_valid(self, obj):
        return obj.is_accreditation_valid()


class BrokerListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for listing brokers.
    """
    branch_name = serializers.SerializerMethodField()
    bd_name = serializers.SerializerMethodField()
    tier_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Broker
        fields = [
            'id', 'name', 'email', 'phone', 'company', 'active',
            'branch_name', 'bd_name', 'tier_name'
        ]
    
    def get_branch_name(self, obj):
        return obj.get_branch_name()
    
    def get_bd_name(self, obj):
        return obj.get_bd_name()
    
    def get_tier_name(self, obj):
        return obj.get_tier_name()


class BrokerCommissionSerializer(serializers.ModelSerializer):
    """
    Serializer for the BrokerCommission model.
    """
    broker_name = serializers.CharField(source='broker.name', read_only=True)
    application_reference = serializers.CharField(source='application.reference_number', read_only=True)
    
    class Meta:
        model = BrokerCommission
        fields = [
            'id', 'broker', 'broker_name', 'application', 'application_reference',
            'amount', 'status', 'description', 'payment_date', 'payment_reference',
            'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class CommissionPaymentItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the CommissionPaymentItem model.
    """
    commission_details = BrokerCommissionSerializer(source='commission', read_only=True)
    
    class Meta:
        model = CommissionPaymentItem
        fields = ['id', 'commission', 'commission_details', 'amount_paid']


class CommissionPaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for the CommissionPayment model.
    """
    items = CommissionPaymentItemSerializer(many=True, read_only=True)
    broker_name = serializers.CharField(source='broker.name', read_only=True)
    
    class Meta:
        model = CommissionPayment
        fields = [
            'id', 'broker', 'broker_name', 'payment_date', 'total_amount',
            'payment_method', 'reference_number', 'notes', 'items',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class CommissionPaymentCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a CommissionPayment with its items.
    """
    commission_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True
    )
    
    class Meta:
        model = CommissionPayment
        fields = [
            'broker', 'payment_date', 'total_amount', 'payment_method',
            'reference_number', 'notes', 'commission_ids'
        ]
    
    def validate(self, data):
        """
        Validate that all commissions belong to the specified broker and are in PENDING status.
        """
        broker = data['broker']
        commission_ids = data.pop('commission_ids')
        
        # Check if all commissions exist and belong to the broker
        commissions = BrokerCommission.objects.filter(id__in=commission_ids, broker=broker)
        if len(commissions) != len(commission_ids):
            raise serializers.ValidationError("Some commissions do not exist or do not belong to this broker")
        
        # Check if all commissions are in PENDING status
        non_pending = commissions.exclude(status='PENDING')
        if non_pending.exists():
            raise serializers.ValidationError("Some commissions are not in PENDING status")
        
        # Calculate total amount and compare with provided total
        calculated_total = sum(commission.amount for commission in commissions)
        if calculated_total != data['total_amount']:
            raise serializers.ValidationError(f"Total amount ({data['total_amount']}) does not match sum of commissions ({calculated_total})")
        
        # Store commissions for create method
        self.commissions = commissions
        
        return data
    
    def create(self, validated_data):
        """
        Create the payment and its items, and update commission statuses.
        """
        payment = CommissionPayment.objects.create(**validated_data)
        
        # Create payment items and update commission statuses
        for commission in self.commissions:
            CommissionPaymentItem.objects.create(
                payment=payment,
                commission=commission,
                amount_paid=commission.amount
            )
            commission.status = 'PAID'
            commission.payment_date = payment.payment_date
            commission.payment_reference = payment.reference_number
            commission.save()
        
        return payment
