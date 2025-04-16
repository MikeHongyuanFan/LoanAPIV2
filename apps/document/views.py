from rest_framework import generics, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
import os
import tempfile

from .models import Document, DocumentTemplate, DocuSignIntegration, DocumentSigningRequest
from .serializers import (
    DocumentSerializer, 
    DocumentUploadSerializer, 
    DocumentGenerateSerializer,
    DocumentTemplateSerializer,
    DocuSignIntegrationSerializer,
    DocumentSigningRequestSerializer,
    DocumentSendForSigningSerializer
)
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

class GenerateDocumentView(views.APIView):
    """
    Generate a document from a template
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = DocumentGenerateSerializer(data=request.data)
        
        if serializer.is_valid():
            application_id = serializer.validated_data['application_id']
            document_type = serializer.validated_data['document_type']
            recipient_type = serializer.validated_data['recipient_type']
            template_data = serializer.validated_data.get('template_data', {})
            
            application = get_object_or_404(Application, id=application_id)
            
            # Get the appropriate template
            try:
                template = DocumentTemplate.objects.get(
                    type=document_type,
                    recipient_type=recipient_type,
                    is_active=True
                )
            except DocumentTemplate.DoesNotExist:
                return Response({
                    "error": f"No active template found for document type '{document_type}' and recipient type '{recipient_type}'"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # In a real implementation, this would use the template to generate a document
            # For now, we'll create a placeholder document record
            
            document = Document.objects.create(
                application=application,
                type=document_type,
                name=f"{template.name} for {application.borrower.name if hasattr(application, 'borrower') and hasattr(application.borrower, 'name') else application.id}",
                description=f"Generated {template.get_type_display()} document for {template.get_recipient_type_display()}"
                # Note: file field is not populated as we're not actually generating a file
            )
            
            return Response({
                "message": "Document generation initiated",
                "document_id": document.id,
                "document_name": document.name,
                "status": "pending"
            }, status=status.HTTP_202_ACCEPTED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DocumentTemplateListView(generics.ListCreateAPIView):
    """
    List all document templates or create a new template
    """
    queryset = DocumentTemplate.objects.all()
    serializer_class = DocumentTemplateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Filter templates based on query parameters
        """
        queryset = DocumentTemplate.objects.all()
        
        # Filter by type
        document_type = self.request.query_params.get('type', None)
        if document_type:
            queryset = queryset.filter(type=document_type)
        
        # Filter by recipient type
        recipient_type = self.request.query_params.get('recipient_type', None)
        if recipient_type:
            queryset = queryset.filter(recipient_type=recipient_type)
        
        # Filter by active status
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            is_active = is_active.lower() == 'true'
            queryset = queryset.filter(is_active=is_active)
            
        return queryset

class DocumentTemplateDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a document template
    """
    queryset = DocumentTemplate.objects.all()
    serializer_class = DocumentTemplateSerializer
    permission_classes = [IsAuthenticated]

class DocuSignIntegrationView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update DocuSign integration settings
    """
    serializer_class = DocuSignIntegrationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        """
        Get the DocuSign integration settings or create default settings
        """
        integration, created = DocuSignIntegration.objects.get_or_create(
            defaults={
                'api_key': '',
                'api_secret': '',
                'integration_key': '',
                'user_id': '',
                'account_id': '',
                'base_url': 'https://demo.docusign.net/restapi',
                'is_active': False
            }
        )
        return integration

class DocumentSendForSigningView(views.APIView):
    """
    Send a document for signing via DocuSign
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = DocumentSendForSigningSerializer(data=request.data)
        
        if serializer.is_valid():
            document_id = serializer.validated_data['document_id']
            recipient_email = serializer.validated_data['recipient_email']
            recipient_name = serializer.validated_data['recipient_name']
            
            document = get_object_or_404(Document, id=document_id)
            
            # Get DocuSign integration settings
            try:
                docusign = DocuSignIntegration.objects.get(is_active=True)
            except DocuSignIntegration.DoesNotExist:
                return Response({
                    "error": "DocuSign integration is not configured"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # In a real implementation, this would use the DocuSign API to send the document
            # For now, we'll create a signing request record
            
            signing_request = DocumentSigningRequest.objects.create(
                document=document,
                recipient_email=recipient_email,
                recipient_name=recipient_name,
                status='SENT',
                docusign_envelope_id=f"mock-envelope-{document.id}"
            )
            
            return Response({
                "message": "Document sent for signing",
                "signing_request_id": signing_request.id,
                "status": signing_request.status
            }, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DocumentSigningRequestListView(generics.ListAPIView):
    """
    List all document signing requests
    """
    serializer_class = DocumentSigningRequestSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Filter signing requests based on query parameters
        """
        queryset = DocumentSigningRequest.objects.all()
        
        # Filter by document
        document_id = self.request.query_params.get('document', None)
        if document_id:
            queryset = queryset.filter(document_id=document_id)
        
        # Filter by status
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status.upper())
        
        # Filter by recipient email
        recipient_email = self.request.query_params.get('recipient_email', None)
        if recipient_email:
            queryset = queryset.filter(recipient_email=recipient_email)
            
        return queryset

class DocumentSigningRequestDetailView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update a document signing request
    """
    queryset = DocumentSigningRequest.objects.all()
    serializer_class = DocumentSigningRequestSerializer
    permission_classes = [IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        """
        Update signing request and handle status changes
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        # If status is changing to COMPLETED, update completed_at timestamp and mark document as signed
        if 'status' in serializer.validated_data and serializer.validated_data['status'] == 'COMPLETED' and instance.status != 'COMPLETED':
            serializer.validated_data['completed_at'] = timezone.now()
            
            # Mark the document as signed
            document = instance.document
            document.is_signed = True
            document.save()
            
        self.perform_update(serializer)
        return Response(serializer.data)

class DocumentsByApplicationView(generics.ListAPIView):
    """
    List all documents for an application
    """
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Filter documents by application
        """
        application_id = self.kwargs['application_id']
        return Document.objects.filter(application_id=application_id)
