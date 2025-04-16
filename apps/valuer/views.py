from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from .models import Valuer
from .serializers import ValuerSerializer, ValuerListSerializer
from apps.application.models import Application
from apps.application.serializers import ApplicationSerializer

class ValuerListView(generics.ListCreateAPIView):
    """
    List all valuers or create a new valuer
    """
    queryset = Valuer.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ValuerListSerializer
        return ValuerSerializer
    
    def get_queryset(self):
        """
        Filter valuers based on query parameters
        """
        queryset = Valuer.objects.all()
        
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

class ValuerDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a valuer
    """
    queryset = Valuer.objects.all()
    serializer_class = ValuerSerializer
    permission_classes = [IsAuthenticated]

class ValuerApplicationsView(generics.ListAPIView):
    """
    List all applications linked to a valuer
    """
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Filter applications by valuer ID
        """
        valuer_id = self.kwargs['pk']
        return Application.objects.filter(valuer_id=valuer_id)
