from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import Application, Note


class ApplicationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for applications.
    """
    queryset = Application.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """
        Submit an application for review.
        """
        application = self.get_object()
        application.status = 'SUBMITTED'
        application.updated_at = timezone.now()
        application.save()
        
        # In a real implementation, we would send notifications here
        
        return Response({
            'status': 'success',
            'message': 'Application submitted successfully'
        })
    
    @action(detail=True, methods=['post'])
    def review(self, request, pk=None):
        """
        Review an application and update its status.
        """
        application = self.get_object()
        status_value = request.data.get('status')
        notes = request.data.get('notes')
        
        if status_value not in [s[0] for s in Application.STATUS_CHOICES]:
            return Response({
                'status': 'error',
                'message': 'Invalid status value'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        application.status = status_value
        application.updated_at = timezone.now()
        application.save()
        
        # Create a note if provided
        if notes:
            Note.objects.create(
                application=application,
                content=notes,
                created_by=request.user
            )
        
        # In a real implementation, we would send notifications here
        
        return Response({
            'status': 'success',
            'message': f'Application status updated to {status_value}'
        })
    
    @action(detail=True, methods=['post'])
    def generate_documents(self, request, pk=None):
        """
        Generate documents for an application.
        """
        application = self.get_object()
        
        # In a real implementation, we would generate actual documents here
        # For now, we'll just return a success message
        
        return Response({
            'status': 'success',
            'message': 'Documents generated successfully',
            'documents': [
                {
                    'id': 1,
                    'name': 'Loan Agreement',
                    'type': 'PDF',
                    'url': f'/media/documents/{application.reference_number}_loan_agreement.pdf'
                },
                {
                    'id': 2,
                    'name': 'Disbursement Letter',
                    'type': 'PDF',
                    'url': f'/media/documents/{application.reference_number}_disbursement_letter.pdf'
                }
            ]
        })
    
    @action(detail=True, methods=['post'])
    def finalize(self, request, pk=None):
        """
        Finalize an application.
        """
        application = self.get_object()
        
        if application.status != 'APPROVED':
            return Response({
                'status': 'error',
                'message': 'Only approved applications can be finalized'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        application.status = 'FINALIZED'
        application.updated_at = timezone.now()
        application.save()
        
        # In a real implementation, we would handle settlement details here
        
        return Response({
            'status': 'success',
            'message': 'Application finalized successfully'
        })


class NoteViewSet(viewsets.ModelViewSet):
    """
    API endpoint for notes.
    """
    queryset = Note.objects.all()
    permission_classes = [permissions.IsAuthenticated]
