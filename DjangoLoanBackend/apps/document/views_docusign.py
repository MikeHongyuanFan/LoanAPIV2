from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings
import json
import base64
import hmac
import hashlib
from datetime import datetime

from .models import Document, DocumentSigningRequest


class DocuSignCallbackView(APIView):
    """
    API endpoint for receiving DocuSign webhook callbacks.
    """
    permission_classes = [AllowAny]  # DocuSign callbacks don't have authentication
    
    def post(self, request):
        # Verify the DocuSign webhook signature if configured
        if not self._verify_docusign_signature(request):
            return Response({"error": "Invalid signature"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Parse the DocuSign event data
        try:
            event_data = request.data
            
            # Extract envelope and document information
            envelope_id = event_data.get('envelopeId')
            status_code = event_data.get('status')
            
            # Find the corresponding signing request
            try:
                signing_request = DocumentSigningRequest.objects.get(envelope_id=envelope_id)
            except DocumentSigningRequest.DoesNotExist:
                return Response({"error": "Unknown envelope ID"}, status=status.HTTP_404_NOT_FOUND)
            
            # Update the signing request status
            signing_request.status = self._map_docusign_status(status_code)
            signing_request.last_updated = datetime.now()
            
            # If completed, update the document status and store the completed document
            if status_code == 'completed':
                signing_request.completed_at = datetime.now()
                
                # Update the document status
                document = signing_request.document
                document.status = 'SIGNED'
                document.save()
                
                # Store the signed document if available in the payload
                if 'documentBase64' in event_data:
                    # This would handle storing the signed document
                    # Implementation depends on how DocuSign returns the document
                    pass
            
            signing_request.save()
            
            return Response({"message": "Webhook processed successfully"}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def _verify_docusign_signature(self, request):
        """
        Verify the DocuSign webhook signature using HMAC.
        """
        # Skip verification if no secret is configured
        if not hasattr(settings, 'DOCUSIGN_WEBHOOK_SECRET'):
            return True
        
        # Get the signature from the headers
        signature = request.headers.get('X-DocuSign-Signature-1')
        if not signature:
            return False
        
        # Get the raw request body
        raw_body = request.body
        
        # Calculate the HMAC signature
        secret = settings.DOCUSIGN_WEBHOOK_SECRET.encode('utf-8')
        computed_signature = base64.b64encode(
            hmac.new(secret, raw_body, digestmod=hashlib.sha256).digest()
        ).decode('utf-8')
        
        # Compare signatures
        return hmac.compare_digest(signature, computed_signature)
    
    def _map_docusign_status(self, docusign_status):
        """
        Map DocuSign status to our internal status.
        """
        status_mapping = {
            'sent': 'SENT',
            'delivered': 'DELIVERED',
            'completed': 'COMPLETED',
            'declined': 'DECLINED',
            'voided': 'CANCELLED',
            'failed': 'FAILED'
        }
        return status_mapping.get(docusign_status.lower(), 'PENDING')


class DocumentVersionView(APIView):
    """
    API endpoint for managing document versions.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, document_id):
        """
        Get all versions of a document.
        """
        try:
            # Get the document
            document = Document.objects.get(id=document_id)
            
            # Get all versions of the document
            versions = Document.objects.filter(
                original_document_id=document.id if document.original_document_id is None else document.original_document_id
            ).order_by('version')
            
            # If the document itself is not linked to an original, include it in the results
            if document.original_document_id is None and document not in versions:
                versions = list(versions)
                versions.insert(0, document)
            
            # Format the response
            version_data = []
            for version in versions:
                version_data.append({
                    'id': version.id,
                    'version': version.version,
                    'filename': version.filename,
                    'status': version.status,
                    'created_at': version.created_at,
                    'created_by': version.created_by.user.username if version.created_by else None,
                    'is_current': version.id == document.id
                })
            
            return Response(version_data)
            
        except Document.DoesNotExist:
            return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request, document_id):
        """
        Create a new version of a document.
        """
        try:
            # Get the original document
            original_document = Document.objects.get(id=document_id)
            
            # Get the highest version number
            highest_version = Document.objects.filter(
                original_document_id=original_document.id if original_document.original_document_id is None else original_document.original_document_id
            ).order_by('-version').first()
            
            new_version = 1
            if highest_version:
                new_version = highest_version.version + 1
            
            # Create a new document as a new version
            new_document = Document.objects.create(
                application=original_document.application,
                document_type=original_document.document_type,
                filename=request.data.get('filename', original_document.filename),
                file=request.data.get('file'),
                status='DRAFT',
                created_by=request.user.profile if hasattr(request.user, 'profile') else None,
                original_document_id=original_document.id if original_document.original_document_id is None else original_document.original_document_id,
                version=new_version
            )
            
            return Response({
                'id': new_document.id,
                'version': new_document.version,
                'filename': new_document.filename,
                'status': new_document.status,
                'created_at': new_document.created_at,
                'message': f"Created new version {new_document.version} of document"
            }, status=status.HTTP_201_CREATED)
            
        except Document.DoesNotExist:
            return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)
