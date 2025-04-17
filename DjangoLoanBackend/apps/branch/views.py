from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Branch
from .serializers import BranchSerializer, BranchListSerializer


class BranchViewSet(viewsets.ModelViewSet):
    """
    API endpoint for branches
    """
    queryset = Branch.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'state', 'country']
    search_fields = ['name', 'code', 'city', 'manager_name']
    ordering_fields = ['name', 'code', 'created_at']
    ordering = ['name']
    
    def get_serializer_class(self):
        """
        Return the serializer class for the request
        """
        if self.action == 'list':
            return BranchListSerializer
        return BranchSerializer
    
    @action(detail=True, methods=['get'])
    def bds(self, request, pk=None):
        """
        Return all BDs associated with this branch
        """
        branch = self.get_object()
        from apps.bd.serializers import BDListSerializer
        from apps.bd.models import BD
        
        bds = BD.objects.filter(branch=branch)
        serializer = BDListSerializer(bds, many=True)
        
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Return all active branches
        """
        branches = Branch.objects.filter(is_active=True)
        serializer = BranchListSerializer(branches, many=True)
        
        return Response(serializer.data)
