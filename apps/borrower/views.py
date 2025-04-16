from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from .models import Borrower
from .serializers import BorrowerSerializer, BorrowerListSerializer
from apps.application.models import Application
from apps.application.serializers import ApplicationSerializer

class BorrowerListView(generics.ListCreateAPIView):
    """
    List all borrowers or create a new borrower
    """
    queryset = Borrower.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BorrowerListSerializer
        return BorrowerSerializer
    
    def get_queryset(self):
        """
        Filter borrowers based on query parameters
        """
        queryset = Borrower.objects.all()
        
        # Filter by state (from address)
        state = self.request.query_params.get('state', None)
        if state:
            queryset = queryset.filter(address__icontains=state)
            
        return queryset

class BorrowerDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a borrower
    """
    queryset = Borrower.objects.all()
    serializer_class = BorrowerSerializer
    permission_classes = [IsAuthenticated]

class BorrowerSearchView(generics.ListAPIView):
    """
    Search borrowers by name, phone, etc.
    """
    serializer_class = BorrowerListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Search borrowers based on query parameters
        """
        queryset = Borrower.objects.all()
        
        # Search term
        search = self.request.query_params.get('q', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(phone__icontains=search) |
                Q(email__icontains=search) |
                Q(address__icontains=search) |
                Q(company_name__icontains=search)
            )
            
        return queryset

class BorrowerApplicationsView(generics.ListAPIView):
    """
    List all applications linked to a borrower
    """
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Filter applications by borrower ID
        """
        borrower_id = self.kwargs['pk']
        return Application.objects.filter(borrower_id=borrower_id)
