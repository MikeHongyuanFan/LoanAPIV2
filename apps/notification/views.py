from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone

from .models import Notification
from .serializers import NotificationSerializer, NotificationCreateSerializer, NotificationSettingsSerializer

class NotificationListView(generics.ListCreateAPIView):
    """
    List all notifications or create a new notification
    """
    queryset = Notification.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NotificationCreateSerializer
        return NotificationSerializer
    
    def get_queryset(self):
        """
        Filter notifications based on query parameters
        """
        queryset = Notification.objects.all()
        
        # Filter by status
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status.upper())
        
        # Filter by type
        notification_type = self.request.query_params.get('type', None)
        if notification_type:
            queryset = queryset.filter(type=notification_type.upper())
        
        # Filter by recipient
        recipient = self.request.query_params.get('recipient', None)
        if recipient:
            queryset = queryset.filter(recipient_email=recipient)
        
        # Filter by related_id
        related_id = self.request.query_params.get('related_id', None)
        if related_id:
            queryset = queryset.filter(related_id=related_id)
            
        return queryset
    
    def perform_create(self, serializer):
        serializer.save()

class NotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a notification
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        """
        Update notification and handle status changes
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        # If status is changing to SENT, update sent_at timestamp
        if 'status' in serializer.validated_data and serializer.validated_data['status'] == 'SENT' and instance.status != 'SENT':
            serializer.validated_data['sent_at'] = timezone.now()
            
        self.perform_update(serializer)
        return Response(serializer.data)

class NotificationSettingsView(APIView):
    """
    Manage notification settings
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Get notification settings
        """
        # This would typically retrieve settings from a database or cache
        # For now, we'll return default settings
        settings = {
            'repayment_reminder_days': 7,
            'loan_expiration_days': 30,
            'stage_stagnation_days': 14,
            'enable_email_notifications': True,
            'enable_sms_notifications': False
        }
        
        return Response(settings, status=status.HTTP_200_OK)
    
    def post(self, request):
        """
        Update notification settings
        """
        serializer = NotificationSettingsSerializer(data=request.data)
        
        if serializer.is_valid():
            # This would typically update settings in a database or cache
            # For now, we'll just return the validated data
            return Response({
                "message": "Settings updated successfully",
                "settings": serializer.validated_data
            }, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
