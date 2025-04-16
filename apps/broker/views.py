from rest_framework import generics, filters, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Broker, BrokerCommission, CommissionPayment
from .serializers import (
    BrokerSerializer, 
    BrokerCommissionSerializer, 
    CommissionPaymentSerializer,
    CommissionPaymentCreateSerializer
)


class BrokerListView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating brokers.
    """
    queryset = Broker.objects.all()
    serializer_class = BrokerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'company', 'email', 'license_number']


class BrokerDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting a broker.
    """
    queryset = Broker.objects.all()
    serializer_class = BrokerSerializer
    permission_classes = [IsAuthenticated]


class BrokerApplicationsView(generics.ListAPIView):
    """
    API endpoint for listing applications linked to a broker.
    """
    serializer_class = None  # Will be imported from application app
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        broker_id = self.kwargs['pk']
        return self.serializer_class.Meta.model.objects.filter(broker_id=broker_id)


class BrokerBorrowersView(generics.ListAPIView):
    """
    API endpoint for listing borrowers linked to a broker.
    """
    serializer_class = None  # Will be imported from borrower app
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        broker_id = self.kwargs['pk']
        return self.serializer_class.Meta.model.objects.filter(applications__broker_id=broker_id).distinct()


class BrokerCommissionListView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating broker commissions.
    """
    serializer_class = BrokerCommissionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'broker']
    search_fields = ['broker__name', 'application__reference_number']
    
    def get_queryset(self):
        return BrokerCommission.objects.all()


class BrokerCommissionDetailView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for retrieving and updating broker commissions.
    """
    queryset = BrokerCommission.objects.all()
    serializer_class = BrokerCommissionSerializer
    permission_classes = [IsAuthenticated]


class BrokerCommissionsView(generics.ListAPIView):
    """
    API endpoint for listing commissions for a specific broker.
    """
    serializer_class = BrokerCommissionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    
    def get_queryset(self):
        broker_id = self.kwargs['pk']
        return BrokerCommission.objects.filter(broker_id=broker_id)


class CommissionPaymentListView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating commission payments.
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['broker']
    search_fields = ['broker__name', 'reference_number']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommissionPaymentCreateSerializer
        return CommissionPaymentSerializer
    
    def get_queryset(self):
        return CommissionPayment.objects.all()


class CommissionPaymentDetailView(generics.RetrieveAPIView):
    """
    API endpoint for retrieving commission payment details.
    """
    queryset = CommissionPayment.objects.all()
    serializer_class = CommissionPaymentSerializer
    permission_classes = [IsAuthenticated]


class BrokerCommissionSummaryView(generics.RetrieveAPIView):
    """
    API endpoint for retrieving a summary of a broker's commissions.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        try:
            broker = Broker.objects.get(pk=pk)
        except Broker.DoesNotExist:
            return Response({"error": "Broker not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Get commission statistics
        total_commissions = BrokerCommission.objects.filter(broker=broker).count()
        pending_commissions = BrokerCommission.objects.filter(broker=broker, status='PENDING').count()
        paid_commissions = BrokerCommission.objects.filter(broker=broker, status='PAID').count()
        cancelled_commissions = BrokerCommission.objects.filter(broker=broker, status='CANCELLED').count()
        
        # Calculate total amounts
        total_amount = BrokerCommission.objects.filter(broker=broker).exclude(status='CANCELLED').aggregate(
            total=models.Sum('amount')
        )['total'] or 0
        
        pending_amount = BrokerCommission.objects.filter(broker=broker, status='PENDING').aggregate(
            total=models.Sum('amount')
        )['total'] or 0
        
        paid_amount = BrokerCommission.objects.filter(broker=broker, status='PAID').aggregate(
            total=models.Sum('amount')
        )['total'] or 0
        
        # Get recent payments
        recent_payments = CommissionPayment.objects.filter(broker=broker).order_by('-payment_date')[:5]
        recent_payments_data = CommissionPaymentSerializer(recent_payments, many=True).data
        
        return Response({
            "broker_id": broker.id,
            "broker_name": broker.name,
            "total_commissions": total_commissions,
            "pending_commissions": pending_commissions,
            "paid_commissions": paid_commissions,
            "cancelled_commissions": cancelled_commissions,
            "total_amount": total_amount,
            "pending_amount": pending_amount,
            "paid_amount": paid_amount,
            "recent_payments": recent_payments_data
        })
