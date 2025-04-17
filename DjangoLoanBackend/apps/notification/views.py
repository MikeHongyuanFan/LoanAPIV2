from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Notification, NotificationSetting

class NotificationListView(generics.ListAPIView):
    """
    List all notifications for the current user
    """
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        # Placeholder - in a real implementation, you would have a proper serializer
        from rest_framework import serializers
        
        class NotificationSerializer(serializers.ModelSerializer):
            class Meta:
                model = Notification
                fields = '__all__'
                
        return NotificationSerializer
    
    def get_queryset(self):
        """
        Filter notifications for the current user
        """
        return Notification.objects.filter(recipient=self.request.user)

class NotificationDetailView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update a notification
    """
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        # Placeholder - in a real implementation, you would have a proper serializer
        from rest_framework import serializers
        
        class NotificationSerializer(serializers.ModelSerializer):
            class Meta:
                model = Notification
                fields = '__all__'
                
        return NotificationSerializer
    
    def get_queryset(self):
        """
        Filter notifications for the current user
        """
        return Notification.objects.filter(recipient=self.request.user)

class NotificationSettingView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update notification settings for the current user
    """
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        # Placeholder - in a real implementation, you would have a proper serializer
        from rest_framework import serializers
        
        class NotificationSettingSerializer(serializers.ModelSerializer):
            class Meta:
                model = NotificationSetting
                fields = '__all__'
                
        return NotificationSettingSerializer
    
    def get_object(self):
        """
        Get notification settings for the current user or create default settings
        """
        settings, created = NotificationSetting.objects.get_or_create(
            user=self.request.user,
            defaults={
                'email_notifications': True,
                'sms_notifications': False,
                'push_notifications': False
            }
        )
        return settings
