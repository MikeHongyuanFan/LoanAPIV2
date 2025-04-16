from rest_framework import generics, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import Notification, NotificationSetting, NotificationTemplate
from .serializers import (
    NotificationSerializer, 
    NotificationCreateSerializer, 
    NotificationSettingSerializer,
    NotificationTemplateSerializer,
    NotificationSettingsUpdateSerializer
)

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

class NotificationSendView(views.APIView):
    """
    Send a notification
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        notification = get_object_or_404(Notification, pk=pk)
        
        if notification.status == 'SENT':
            return Response({
                "message": "Notification has already been sent"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        success = notification.send()
        
        if success:
            return Response({
                "message": "Notification sent successfully",
                "notification": NotificationSerializer(notification).data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "Failed to send notification"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class NotificationSettingListView(generics.ListCreateAPIView):
    """
    List all notification settings or create a new setting
    """
    queryset = NotificationSetting.objects.all()
    serializer_class = NotificationSettingSerializer
    permission_classes = [IsAuthenticated]

class NotificationSettingDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a notification setting
    """
    queryset = NotificationSetting.objects.all()
    serializer_class = NotificationSettingSerializer
    permission_classes = [IsAuthenticated]

class NotificationTemplateListView(generics.ListCreateAPIView):
    """
    List all notification templates or create a new template
    """
    queryset = NotificationTemplate.objects.all()
    serializer_class = NotificationTemplateSerializer
    permission_classes = [IsAuthenticated]

class NotificationTemplateDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a notification template
    """
    queryset = NotificationTemplate.objects.all()
    serializer_class = NotificationTemplateSerializer
    permission_classes = [IsAuthenticated]

class NotificationSettingsUpdateView(views.APIView):
    """
    Update multiple notification settings at once
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Get all notification settings as a dictionary
        """
        settings = {}
        
        # Get all settings from the database
        notification_settings = NotificationSetting.objects.all()
        
        # Convert to a dictionary format
        for setting in notification_settings:
            if setting.setting_type == 'REPAYMENT_REMINDER_DAYS':
                settings['repayment_reminder_days'] = setting.value
            elif setting.setting_type == 'LOAN_EXPIRATION_DAYS':
                settings['loan_expiration_days'] = setting.value
            elif setting.setting_type == 'LATE_REPAYMENT_DAYS':
                settings['late_repayment_days'] = setting.value
            elif setting.setting_type == 'STAGE_STAGNATION_DAYS':
                settings['stage_stagnation_days'] = setting.value
        
        return Response(settings, status=status.HTTP_200_OK)
    
    def post(self, request):
        """
        Update multiple notification settings at once
        """
        serializer = NotificationSettingsUpdateSerializer(data=request.data)
        
        if serializer.is_valid():
            # Update each setting in the database
            for key, value in serializer.validated_data.items():
                if key == 'repayment_reminder_days':
                    setting_type = 'REPAYMENT_REMINDER_DAYS'
                elif key == 'loan_expiration_days':
                    setting_type = 'LOAN_EXPIRATION_DAYS'
                elif key == 'late_repayment_days':
                    setting_type = 'LATE_REPAYMENT_DAYS'
                elif key == 'stage_stagnation_days':
                    setting_type = 'STAGE_STAGNATION_DAYS'
                else:
                    continue
                
                # Update or create the setting
                setting, created = NotificationSetting.objects.update_or_create(
                    setting_type=setting_type,
                    defaults={'value': value}
                )
            
            return Response({
                "message": "Settings updated successfully",
                "settings": serializer.validated_data
            }, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PendingNotificationsView(views.APIView):
    """
    Process pending notifications
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Process all pending notifications that are due
        """
        now = timezone.now()
        
        # Get all pending notifications that are due
        pending_notifications = Notification.objects.filter(
            status='PENDING',
            trigger_date__lte=now
        )
        
        sent_count = 0
        failed_count = 0
        
        # Send each notification
        for notification in pending_notifications:
            success = notification.send()
            if success:
                sent_count += 1
            else:
                failed_count += 1
        
        return Response({
            "message": f"Processed {sent_count + failed_count} notifications",
            "sent": sent_count,
            "failed": failed_count
        }, status=status.HTTP_200_OK)
