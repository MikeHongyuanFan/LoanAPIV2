from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from .models import Broker
from .serializers import BrokerSerializer, BrokerListSerializer
from apps.application.models import Application
from apps.application.serializers import ApplicationSerializer
from apps.borrower.models import Borrower
from apps.borrower.serializers import BorrowerListSerializer

class BrokerListView(generics.ListCreateAPIView):
    """
    List all brokers or create a new broker
    """
    queryset = Broker.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BrokerListSerializer
        return BrokerSerializer
    
    def get_queryset(self):
        """
        Filter brokers based on query parameters
        """
        queryset = Broker.objects.all()
        
        # Search term
        search = self.request.query_params.get('q', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(company__icontains=search) |
                Q(email__icontains=search) |
                Q(phone__icontains=search)
            )
            
        return queryset

class BrokerDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a broker
    """
    queryset = Broker.objects.all()
    serializer_class = BrokerSerializer
    permission_classes = [IsAuthenticated]

class BrokerApplicationsView(generics.ListAPIView):
    """
    List all applications linked to a broker
    """
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Filter applications by broker ID
        """
        broker_id = self.kwargs['pk']
        return Application.objects.filter(broker_id=broker_id)

class BrokerBorrowersView(generics.ListAPIView):
    """
    List all borrowers linked to a broker
    """
    serializer_class = BorrowerListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Filter borrowers by broker ID
        """
        broker_id = self.kwargs['pk']
        return Borrower.objects.filter(broker_id=broker_id)
