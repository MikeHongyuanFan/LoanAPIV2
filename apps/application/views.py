from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Application, Note, Repayment, Extension
from .serializers import (
    ApplicationSerializer, 
    ApplicationDetailSerializer,
    NoteSerializer,
    RepaymentSerializer,
    ExtensionSerializer,
    LoanCalculatorSerializer
)

class ApplicationListView(generics.ListCreateAPIView):
    """
    List all applications or create a new application
    """
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Filter applications based on query parameters
        """
        queryset = Application.objects.all()
        
        # Filter by keywords
        keyword = self.request.query_params.get('keyword', None)
        if keyword:
            queryset = queryset.filter(
                borrower__name__icontains=keyword
            ) | queryset.filter(
                property_address__icontains=keyword
            )
        
        # Filter by stage
        stage = self.request.query_params.get('stage', None)
        if stage:
            queryset = queryset.filter(stage=stage)
        
        # Filter by broker
        broker_id = self.request.query_params.get('broker', None)
        if broker_id:
            queryset = queryset.filter(broker_id=broker_id)
        
        # Filter by product (loan type)
        product_id = self.request.query_params.get('product', None)
        if product_id:
            queryset = queryset.filter(product_id=product_id)
            
        return queryset

class ApplicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete an application
    """
    queryset = Application.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ApplicationDetailSerializer
        return ApplicationSerializer

class ApplicationDocumentView(views.APIView):
    """
    Upload documents to an application
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        application = get_object_or_404(Application, pk=pk)
        
        # This would typically call the Document service
        # For now, we'll just return a success response
        return Response({
            "message": "Document upload endpoint. Integration with Document service required."
        }, status=status.HTTP_200_OK)

class GenerateDocumentView(views.APIView):
    """
    Generate documents for an application
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        application = get_object_or_404(Application, pk=pk)
        
        # This would typically call the Document service to generate documents
        # For now, we'll just return a success response
        return Response({
            "message": "Document generation endpoint. Integration with Document service required."
        }, status=status.HTTP_200_OK)

class NoteCreateView(generics.CreateAPIView):
    """
    Create a note for an application
    """
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        application = get_object_or_404(Application, pk=self.kwargs['pk'])
        serializer.save(
            application=application,
            created_by=self.request.user
        )

class LoanCalculatorView(views.APIView):
    """
    Calculate loan amounts and fees
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        application = get_object_or_404(Application, pk=pk)
        serializer = LoanCalculatorSerializer(data=request.data)
        
        if serializer.is_valid():
            data = serializer.validated_data
            result = {}
            
            # Calculate based on gross loan amount
            if 'gross_loan_amount' in data:
                gross_amount = data['gross_loan_amount']
                fees = data.get('fees', 0)
                net_amount = gross_amount - fees
                result = {
                    'gross_loan_amount': gross_amount,
                    'fees': fees,
                    'net_loan_amount': net_amount
                }
            
            # Calculate based on net loan amount
            elif 'net_loan_amount' in data:
                net_amount = data['net_loan_amount']
                fees = data.get('fees', 0)
                gross_amount = net_amount + fees
                result = {
                    'gross_loan_amount': gross_amount,
                    'fees': fees,
                    'net_loan_amount': net_amount
                }
                
            return Response(result, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RepaymentCreateView(generics.CreateAPIView):
    """
    Create a repayment for an application
    """
    serializer_class = RepaymentSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        application = get_object_or_404(Application, pk=self.kwargs['pk'])
        serializer.save(application=application)

class ExtensionCreateView(generics.CreateAPIView):
    """
    Create a loan extension for an application
    """
    serializer_class = ExtensionSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        application = get_object_or_404(Application, pk=self.kwargs['pk'])
        serializer.save(application=application)
