from rest_framework import generics, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import Product
from .serializers import ProductSerializer, ProductListSerializer

class ProductListView(generics.ListCreateAPIView):
    """
    List all loan products or create a new loan product
    """
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductListSerializer
        return ProductSerializer
    
    def get_queryset(self):
        """
        Filter products based on query parameters
        """
        queryset = Product.objects.all()
        
        # Filter by active status
        active = self.request.query_params.get('active', None)
        if active is not None:
            is_active = active.lower() == 'true'
            queryset = queryset.filter(is_active=is_active)
        
        # Filter by interest rate range
        min_rate = self.request.query_params.get('min_rate', None)
        if min_rate is not None:
            queryset = queryset.filter(interest_rate__gte=float(min_rate))
            
        max_rate = self.request.query_params.get('max_rate', None)
        if max_rate is not None:
            queryset = queryset.filter(interest_rate__lte=float(max_rate))
        
        # Search by name or description
        search = self.request.query_params.get('q', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )
            
        return queryset

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a loan product
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

class ProductDocumentsView(APIView):
    """
    Manage documents required for a loan product
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        """
        List documents required for a loan product
        """
        product = get_object_or_404(Product, pk=pk)
        
        # This would typically call the Document service to get required documents
        # For now, we'll just return a placeholder response
        return Response({
            "message": "Document requirements endpoint. Integration with Document service required.",
            "product_id": str(product.id),
            "product_name": product.name
        }, status=status.HTTP_200_OK)
    
    def post(self, request, pk):
        """
        Add document requirements to a loan product
        """
        product = get_object_or_404(Product, pk=pk)
        
        # This would typically call the Document service to add document requirements
        # For now, we'll just return a success response
        return Response({
            "message": "Document requirements updated. Integration with Document service required.",
            "product_id": str(product.id)
        }, status=status.HTTP_200_OK)
