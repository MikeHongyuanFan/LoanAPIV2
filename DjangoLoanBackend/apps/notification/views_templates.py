from rest_framework import generics, views, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.template import Template, Context
from django.utils import timezone

from .models import NotificationTemplate
from apps.application.models import Application

class NotificationTemplateListView(generics.ListCreateAPIView):
    """
    List all notification templates or create a new template
    """
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        from rest_framework import serializers
        
        class NotificationTemplateSerializer(serializers.ModelSerializer):
            class Meta:
                model = NotificationTemplate
                fields = '__all__'
                
        return NotificationTemplateSerializer
    
    def get_queryset(self):
        return NotificationTemplate.objects.all()

class NotificationTemplateDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a notification template
    """
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        from rest_framework import serializers
        
        class NotificationTemplateSerializer(serializers.ModelSerializer):
            class Meta:
                model = NotificationTemplate
                fields = '__all__'
                
        return NotificationTemplateSerializer
    
    def get_queryset(self):
        return NotificationTemplate.objects.all()

class NotificationTemplatePreviewView(views.APIView):
    """
    Preview a notification template with sample data
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Generate a preview of a notification template with sample data
        """
        template_id = request.data.get('template_id')
        application_id = request.data.get('application_id')
        
        try:
            template = NotificationTemplate.objects.get(id=template_id)
        except NotificationTemplate.DoesNotExist:
            return Response({"error": "Template not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Get sample data
        context_data = self._get_sample_data(template.type, application_id)
        
        # Render the template
        try:
            subject_template = Template(template.subject_template)
            body_template = Template(template.body_template)
            
            context = Context(context_data)
            
            rendered_subject = subject_template.render(context)
            rendered_body = body_template.render(context)
            
            return Response({
                "subject": rendered_subject,
                "body": rendered_body,
                "template_type": template.type,
                "template_name": template.name
            })
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def _get_sample_data(self, template_type, application_id=None):
        """
        Get sample data for the template based on its type
        """
        # Base context with common variables
        context = {
            "current_date": timezone.now().strftime("%Y-%m-%d"),
            "company_name": "Loan Application System",
            "support_email": "support@loanapplication.com",
            "support_phone": "1-800-123-4567"
        }
        
        # Try to get a real application if ID is provided
        application = None
        if application_id:
            try:
                application = Application.objects.get(id=application_id)
            except Application.DoesNotExist:
                pass
        
        # Add template-specific variables
        if template_type == 'STAGE_CHANGE':
            if application:
                context.update({
                    "application_id": application.id,
                    "reference_number": application.reference_number,
                    "stage": application.get_status_display(),
                    "borrower_name": application.borrower.name if application.borrower else "John Doe",
                    "loan_amount": application.loan_amount,
                    "interest_rate": application.interest_rate,
                    "property_address": application.property_address,
                })
            else:
                context.update({
                    "application_id": "APP-123456",
                    "reference_number": "APP-202504-ABC123",
                    "stage": "Under Review",
                    "borrower_name": "John Doe",
                    "loan_amount": "$250,000",
                })
                
        elif template_type == 'STAGE_STAGNATION':
            context.update({
                "application_id": "APP-123456" if not application else application.id,
                "reference_number": "APP-202504-ABC123" if not application else application.reference_number,
                "stage": "Under Review" if not application else application.get_status_display(),
                "days": 14,
                "last_updated": (timezone.now() - timezone.timedelta(days=14)).strftime("%Y-%m-%d"),
            })
            
        elif template_type == 'NOTE_REMINDER':
            context.update({
                "application_id": "APP-123456" if not application else application.id,
                "reference_number": "APP-202504-ABC123" if not application else application.reference_number,
                "note_content": "Follow up with borrower about missing documents",
                "reminder_date": timezone.now().strftime("%Y-%m-%d"),
                "created_by": "Jane Smith",
            })
            
        elif template_type in ['REPAYMENT_REMINDER', 'LATE_REPAYMENT']:
            context.update({
                "application_id": "APP-123456" if not application else application.id,
                "reference_number": "APP-202504-ABC123" if not application else application.reference_number,
                "due_date": (timezone.now() + timezone.timedelta(days=7)).strftime("%Y-%m-%d"),
                "amount": "$1,250.00",
                "days": 7 if template_type == 'REPAYMENT_REMINDER' else 3,
                "payment_link": "https://loanapplication.com/payments/APP-123456",
            })
            
        elif template_type == 'LOAN_EXPIRATION':
            context.update({
                "application_id": "APP-123456" if not application else application.id,
                "reference_number": "APP-202504-ABC123" if not application else application.reference_number,
                "expiry_date": (timezone.now() + timezone.timedelta(days=30)).strftime("%Y-%m-%d"),
                "days": 30,
                "borrower_name": "John Doe" if not application else (application.borrower.full_name if application.borrower else "John Doe"),
                "loan_amount": "$250,000" if not application else application.loan_amount,
            })
            
        elif template_type in ['EXTENSION_REQUEST', 'EXTENSION_STATUS']:
            context.update({
                "application_id": "APP-123456" if not application else application.id,
                "reference_number": "APP-202504-ABC123" if not application else application.reference_number,
                "original_expiry_date": (timezone.now() + timezone.timedelta(days=15)).strftime("%Y-%m-%d"),
                "new_expiry_date": (timezone.now() + timezone.timedelta(days=45)).strftime("%Y-%m-%d"),
                "reason": "Cash flow issues due to delayed project completion",
                "status": "APPROVED" if template_type == 'EXTENSION_STATUS' else "PENDING",
                "fee_amount": "$500.00",
            })
            
        elif template_type == 'FEE_STATUS':
            context.update({
                "application_id": "APP-123456" if not application else application.id,
                "reference_number": "APP-202504-ABC123" if not application else application.reference_number,
                "fee_type": "Establishment Fee",
                "amount": "$2,500.00",
                "status": "PAID",
                "payment_date": timezone.now().strftime("%Y-%m-%d"),
            })
            
        return context

class SendEmailNotificationView(views.APIView):
    """
    Send an email notification using a template
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Send an email notification using a template
        """
        template_id = request.data.get('template_id')
        application_id = request.data.get('application_id')
        recipient_email = request.data.get('recipient_email')
        custom_data = request.data.get('custom_data', {})
        
        if not template_id or not recipient_email:
            return Response({"error": "Template ID and recipient email are required"}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        try:
            template = NotificationTemplate.objects.get(id=template_id)
        except NotificationTemplate.DoesNotExist:
            return Response({"error": "Template not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Get data for the template
        if application_id:
            try:
                application = Application.objects.get(id=application_id)
                context_data = self._get_application_data(template.type, application)
            except Application.DoesNotExist:
                return Response({"error": "Application not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            context_data = {}
        
        # Add custom data
        context_data.update(custom_data)
        
        # Render the template
        try:
            subject_template = Template(template.subject_template)
            body_template = Template(template.body_template)
            
            context = Context(context_data)
            
            rendered_subject = subject_template.render(context)
            rendered_body = body_template.render(context)
            
            # Create notification record
            from .models import Notification
            notification = Notification.objects.create(
                type=template.type,
                recipient_email=recipient_email,
                subject=rendered_subject,
                message=rendered_body,
                template=template,
                related_entity='Application' if application_id else None,
                related_id=application_id,
                created_by=request.user.profile if hasattr(request.user, 'profile') else None
            )
            
            # Send the email
            notification.send()
            
            return Response({
                "message": "Email notification sent successfully",
                "notification_id": notification.id
            })
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def _get_application_data(self, template_type, application):
        """
        Get data for the template based on a real application
        """
        # Base context with common variables
        context = {
            "current_date": timezone.now().strftime("%Y-%m-%d"),
            "company_name": "Loan Application System",
            "support_email": "support@loanapplication.com",
            "support_phone": "1-800-123-4567",
            "application_id": application.id,
            "reference_number": application.reference_number,
        }
        
        # Add borrower information if available
        if application.borrower:
            context.update({
                "borrower_name": application.borrower.name,
                "borrower_email": application.borrower.email,
                "borrower_phone": application.borrower.phone,
            })
        
        # Add loan details
        context.update({
            "loan_amount": application.loan_amount,
            "interest_rate": application.interest_rate,
            "loan_term": application.loan_term_months,
            "stage": application.get_status_display(),
        })
        
        # Add property details if available
        if hasattr(application, 'property_address') and application.property_address:
            context.update({
                "property_address": application.property_address,
                "property_value": application.property_value,
            })
        
        return context
