from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Broker, BrokerCommission, CommissionPayment, BrokerTier, BrokerSpecialization
from .serializers import (
    BrokerSerializer, BrokerListSerializer, BrokerCommissionSerializer,
    CommissionPaymentSerializer, CommissionPaymentCreateSerializer,
    BrokerTierSerializer, BrokerSpecializationSerializer
)


class BrokerTierViewSet(viewsets.ModelViewSet):
    """
    API endpoint for broker tiers
    """
    queryset = BrokerTier.objects.all()
    serializer_class = BrokerTierSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'commission_multiplier', 'created_at']
    ordering = ['name']


class BrokerSpecializationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for broker specializations
    """
    queryset = BrokerSpecialization.objects.all()
    serializer_class = BrokerSpecializationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class BrokerViewSet(viewsets.ModelViewSet):
    """
    API endpoint for brokers
    """
    queryset = Broker.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['active', 'branch', 'bd', 'tier', 'specializations']
    search_fields = ['name', 'email', 'company', 'license_number']
    ordering_fields = ['name', 'company', 'created_at']
    ordering = ['name']
    
    def get_serializer_class(self):
        """
        Return the serializer class for the request
        """
        if self.action == 'list':
            return BrokerListSerializer
        return BrokerSerializer
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Return all active brokers
        """
        brokers = Broker.objects.filter(active=True)
        serializer = BrokerListSerializer(brokers, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_branch(self, request):
        """
        Return brokers grouped by branch
        """
        from apps.branch.models import Branch
        from apps.branch.serializers import BranchListSerializer
        
        branches = Branch.objects.all()
        result = []
        
        for branch in branches:
            brokers = Broker.objects.filter(branch=branch)
            branch_data = BranchListSerializer(branch).data
            branch_data['brokers'] = BrokerListSerializer(brokers, many=True).data
            result.append(branch_data)
        
        return Response(result)
    
    @action(detail=False, methods=['get'])
    def by_bd(self, request):
        """
        Return brokers grouped by BD
        """
        from apps.bd.models import BD
        from apps.bd.serializers import BDListSerializer
        
        bds = BD.objects.all()
        result = []
        
        for bd in bds:
            brokers = Broker.objects.filter(bd=bd)
            bd_data = BDListSerializer(bd).data
            bd_data['brokers'] = BrokerListSerializer(brokers, many=True).data
            result.append(bd_data)
        
        return Response(result)
    
    @action(detail=False, methods=['get'])
    def by_tier(self, request):
        """
        Return brokers grouped by tier
        """
        tiers = BrokerTier.objects.all()
        result = []
        
        for tier in tiers:
            brokers = Broker.objects.filter(tier=tier)
            tier_data = BrokerTierSerializer(tier).data
            tier_data['brokers'] = BrokerListSerializer(brokers, many=True).data
            result.append(tier_data)
        
        # Add brokers with no tier
        brokers_no_tier = Broker.objects.filter(tier__isnull=True)
        if brokers_no_tier.exists():
            result.append({
                'id': None,
                'name': 'No Tier',
                'brokers': BrokerListSerializer(brokers_no_tier, many=True).data
            })
        
        return Response(result)
    
    @action(detail=True, methods=['get'])
    def commissions(self, request, pk=None):
        """
        Return all commissions for a broker
        """
        broker = self.get_object()
        commissions = BrokerCommission.objects.filter(broker=broker)
        serializer = BrokerCommissionSerializer(commissions, many=True)
        return Response(serializer.data)


class BrokerCommissionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for broker commissions
    """
    queryset = BrokerCommission.objects.all()
    serializer_class = BrokerCommissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['broker', 'status', 'payment_date']
    search_fields = ['broker__name', 'application__reference_number']
    ordering_fields = ['created_at', 'amount', 'payment_date']
    ordering = ['-created_at']


class CommissionPaymentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for commission payments
    """
    queryset = CommissionPayment.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['broker', 'payment_date', 'payment_method']
    search_fields = ['broker__name', 'reference_number']
    ordering_fields = ['payment_date', 'total_amount']
    ordering = ['-payment_date']
    
    def get_serializer_class(self):
        """
        Return the serializer class for the request
        """
        if self.action == 'create':
            return CommissionPaymentCreateSerializer
        return CommissionPaymentSerializer
