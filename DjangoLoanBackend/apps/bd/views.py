from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import BD
from .serializers import BDSerializer, BDListSerializer


class BDViewSet(viewsets.ModelViewSet):
    """
    API endpoint for BDs
    """
    queryset = BD.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'branch', 'position']
    search_fields = ['first_name', 'last_name', 'email', 'employee_id']
    ordering_fields = ['last_name', 'first_name', 'hire_date', 'created_at']
    ordering = ['last_name', 'first_name']
    
    def get_serializer_class(self):
        """
        Return the serializer class for the request
        """
        if self.action == 'list':
            return BDListSerializer
        return BDSerializer
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Return all active BDs
        """
        bds = BD.objects.filter(is_active=True)
        serializer = BDListSerializer(bds, many=True)
        
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_branch(self, request):
        """
        Return BDs grouped by branch
        """
        from collections import defaultdict
        from apps.branch.models import Branch
        from apps.branch.serializers import BranchListSerializer
        
        branches = Branch.objects.all()
        result = []
        
        for branch in branches:
            bds = BD.objects.filter(branch=branch)
            branch_data = BranchListSerializer(branch).data
            branch_data['bds'] = BDListSerializer(bds, many=True).data
            result.append(branch_data)
        
        return Response(result)
