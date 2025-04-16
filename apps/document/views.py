from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import Document
from .serializers import DocumentSerializer, DocumentUploadSerializer, DocumentGenerateSerializer
from apps.application.models import Application

class DocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a document
    """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

class UploadDocumentView(generics.CreateAPIView):
    """
    Upload a new document
    """
    serializer_class = DocumentUploadSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save()
        
        # Notify relevant parties about the document upload
        # This would typically call the Notification service
        application = serializer.validated_data['application']
        document_type = serializer.validated_data['type']
        document_name = serializer.validated_data['name']
        
        # Log the document upload
        print(f"Document uploaded: {document_name} ({document_type}) for application {application.id}")

class GenerateDocumentView(APIView):
    """
    Generate a document from a template
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = DocumentGenerateSerializer(data=request.data)
        
        if serializer.is_valid():
            application_id = serializer.validated_data['application_id']
            document_type = serializer.validated_data['document_type']
            template_data = serializer.validated_data.get('template_data', {})
            
            application = get_object_or_404(Application, id=application_id)
            
            # This would typically call a document generation service
            # For now, we'll just create a placeholder document record
            
            document = Document.objects.create(
                application=application,
                type=document_type,
                name=f"{document_type} for {application.id}",
                description=f"Generated {document_type} document"
                # Note: file field is not populated as we're not actually generating a file
            )
            
            return Response({
                "message": "Document generation initiated",
                "document_id": document.id,
                "status": "pending"
            }, status=status.HTTP_202_ACCEPTED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
