from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from .models import QS
from .serializers import QSSerializer, QSListSerializer
from apps.application.models import Application
from apps.application.serializers import ApplicationSerializer

class QSListView(generics.ListCreateAPIView):
    """
    List all quantity surveyors or create a new quantity surveyor
    """
    queryset = QS.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return QSListSerializer
        return QSSerializer
    
    def get_queryset(self):
        """
        Filter quantity surveyors based on query parameters
        """
        queryset = QS.objects.all()
        
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

class QSDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a quantity surveyor
    """
    queryset = QS.objects.all()
    serializer_class = QSSerializer
    permission_classes = [IsAuthenticated]

class QSApplicationsView(generics.ListAPIView):
    """
    List all applications linked to a quantity surveyor
    """
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Filter applications by quantity surveyor ID
        """
        qs_id = self.kwargs['pk']
        return Application.objects.filter(qs_id=qs_id)
