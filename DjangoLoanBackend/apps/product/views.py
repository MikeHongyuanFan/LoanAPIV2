from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Product, ProductDocumentRequirement

class ProductListCreateView(generics.ListCreateAPIView):
    """
    List all products or create a new product
    """
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        # Placeholder - in a real implementation, you would have a proper serializer
        from rest_framework import serializers
        
        class ProductSerializer(serializers.ModelSerializer):
            class Meta:
                model = Product
                fields = '__all__'
                
        return ProductSerializer

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a product
    """
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        # Placeholder - in a real implementation, you would have a proper serializer
        from rest_framework import serializers
        
        class ProductSerializer(serializers.ModelSerializer):
            class Meta:
                model = Product
                fields = '__all__'
                
        return ProductSerializer

class ProductDocumentRequirementListView(generics.ListCreateAPIView):
    """
    List all document requirements for a product or create a new requirement
    """
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        # Placeholder - in a real implementation, you would have a proper serializer
        from rest_framework import serializers
        
        class ProductDocumentRequirementSerializer(serializers.ModelSerializer):
            class Meta:
                model = ProductDocumentRequirement
                fields = '__all__'
                
        return ProductDocumentRequirementSerializer
    
    def get_queryset(self):
        """
        Filter requirements by product
        """
        product_id = self.kwargs['product_id']
        return ProductDocumentRequirement.objects.filter(product_id=product_id)
    
    def perform_create(self, serializer):
        """
        Set the product when creating a new requirement
        """
        product_id = self.kwargs['product_id']
        serializer.save(product_id=product_id)

class ProductDocumentRequirementDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a document requirement
    """
    queryset = ProductDocumentRequirement.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        # Placeholder - in a real implementation, you would have a proper serializer
        from rest_framework import serializers
        
        class ProductDocumentRequirementSerializer(serializers.ModelSerializer):
            class Meta:
                model = ProductDocumentRequirement
                fields = '__all__'
                
        return ProductDocumentRequirementSerializer
