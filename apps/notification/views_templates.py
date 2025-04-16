from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.template import Template, Context
from django.core.mail import send_mail
from django.conf import settings

from .models import NotificationTemplate, Notification
from .serializers import NotificationTemplateSerializer
from apps.authentication.permissions import IsManager, IsStaff


class NotificationTemplateListView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating notification templates.
    """
    queryset = NotificationTemplate.objects.all()
    serializer_class = NotificationTemplateSerializer
    permission_classes = [IsAuthenticated, IsStaff]


class NotificationTemplateDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting a notification template.
    """
    queryset = NotificationTemplate.objects.all()
    serializer_class = NotificationTemplateSerializer
    permission_classes = [IsAuthenticated, IsStaff]


class NotificationTemplatePreviewView(APIView):
    """
    API endpoint for previewing a notification template with sample data.
    """
    permission_classes = [IsAuthenticated, IsStaff]
    
    def post(self, request, pk):
        try:
            # Get the template
            template = NotificationTemplate.objects.get(pk=pk)
            
            # Get sample data from request or use defaults
            sample_data = request.data.get('sample_data', {})
            
            # Provide default sample data if not provided
            default_data = {
                'application': {
                    'reference_number': 'APP12345',
                    'loan_amount': 250000,
                    'status': 'APPROVED',
                    'stage': 'SETTLEMENT'
                },
                'borrower': {
                    'name': 'John Smith',
                    'email': 'john.smith@example.com',
                    'phone': '1234567890'
                },
                'broker': {
                    'name': 'Jane Broker',
                    'company': 'ABC Brokers',
                    'email': 'jane@abcbrokers.com'
                },
                'user': {
                    'name': 'Admin User',
                    'email': 'admin@example.com'
                },
                'date': '2025-04-16',
                'time': '10:30 AM',
                'url': 'https://example.com/application/APP12345'
            }
            
            # Merge provided sample data with defaults
            for key, value in default_data.items():
                if key not in sample_data:
                    sample_data[key] = value
                elif isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        if sub_key not in sample_data[key]:
                            sample_data[key][sub_key] = sub_value
            
            # Render the template subject and body
            subject_template = Template(template.subject)
            body_template = Template(template.body)
            
            context = Context(sample_data)
            rendered_subject = subject_template.render(context)
            rendered_body = body_template.render(context)
            
            return Response({
                'template_id': template.id,
                'template_name': template.name,
                'rendered_subject': rendered_subject,
                'rendered_body': rendered_body,
                'sample_data': sample_data
            })
            
        except NotificationTemplate.DoesNotExist:
            return Response({"error": "Template not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SendTestNotificationView(APIView):
    """
    API endpoint for sending a test notification using a template.
    """
    permission_classes = [IsAuthenticated, IsManager]
    
    def post(self, request, pk):
        try:
            # Get the template
            template = NotificationTemplate.objects.get(pk=pk)
            
            # Get recipient email
            recipient_email = request.data.get('recipient_email')
            if not recipient_email:
                return Response({"error": "Recipient email is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Get sample data from request or use defaults
            sample_data = request.data.get('sample_data', {})
            
            # Provide default sample data if not provided
            default_data = {
                'application': {
                    'reference_number': 'APP12345',
                    'loan_amount': 250000,
                    'status': 'APPROVED',
                    'stage': 'SETTLEMENT'
                },
                'borrower': {
                    'name': 'John Smith',
                    'email': 'john.smith@example.com',
                    'phone': '1234567890'
                },
                'broker': {
                    'name': 'Jane Broker',
                    'company': 'ABC Brokers',
                    'email': 'jane@abcbrokers.com'
                },
                'user': {
                    'name': 'Admin User',
                    'email': 'admin@example.com'
                },
                'date': '2025-04-16',
                'time': '10:30 AM',
                'url': 'https://example.com/application/APP12345'
            }
            
            # Merge provided sample data with defaults
            for key, value in default_data.items():
                if key not in sample_data:
                    sample_data[key] = value
                elif isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        if sub_key not in sample_data[key]:
                            sample_data[key][sub_key] = sub_value
            
            # Render the template subject and body
            subject_template = Template(template.subject)
            body_template = Template(template.body)
            
            context = Context(sample_data)
            rendered_subject = subject_template.render(context)
            rendered_body = body_template.render(context)
            
            # Send the test email
            send_mail(
                subject=rendered_subject,
                message=rendered_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient_email],
                fail_silently=False,
                html_message=rendered_body if template.is_html else None
            )
            
            # Create a notification record
            Notification.objects.create(
                type='TEST',
                recipient_email=recipient_email,
                subject=rendered_subject,
                message=rendered_body,
                status='SENT',
                template=template,
                created_by=request.user.profile if hasattr(request.user, 'profile') else None
            )
            
            return Response({
                'message': f"Test notification sent to {recipient_email}",
                'subject': rendered_subject
            })
            
        except NotificationTemplate.DoesNotExist:
            return Response({"error": "Template not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SMSNotificationView(APIView):
    """
    API endpoint for sending SMS notifications.
    """
    permission_classes = [IsAuthenticated, IsStaff]
    
    def post(self, request):
        # Get recipient phone number
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({"error": "Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get message
        message = request.data.get('message')
        if not message:
            return Response({"error": "Message is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # In a real implementation, this would integrate with an SMS service provider
        # For now, we'll just create a notification record
        
        # Create a notification record
        notification = Notification.objects.create(
            type='SMS',
            recipient_phone=phone_number,
            message=message,
            status='PENDING',
            created_by=request.user.profile if hasattr(request.user, 'profile') else None
        )
        
        # In a real implementation, we would send the SMS here
        # For now, we'll just simulate it
        notification.status = 'SENT'
        notification.save()
        
        return Response({
            'message': f"SMS notification queued for {phone_number}",
            'notification_id': notification.id
        })
