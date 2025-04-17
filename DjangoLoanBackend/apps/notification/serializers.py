from rest_framework import serializers
from .models import Notification, NotificationSetting, NotificationTemplate

class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for notification information
    """
    class Meta:
        model = Notification
        fields = [
            'id', 'type', 'recipient_email', 'related_id', 'trigger_date', 
            'created_at', 'subject', 'message', 'status', 'sent_at'
        ]
        read_only_fields = ['id', 'created_at', 'sent_at']

class NotificationCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating notifications
    """
    class Meta:
        model = Notification
        fields = ['type', 'recipient_email', 'related_id', 'trigger_date', 'subject', 'message']
        
    def validate(self, data):
        """
        Validate that the trigger date is not in the past
        """
        if data.get('trigger_date') and data['trigger_date'] < serializers.DateTimeField().to_representation(serializers.DateTimeField().to_internal_value('2025-04-16T09:43:11Z')):
            raise serializers.ValidationError("Trigger date cannot be in the past")
        return data

class NotificationSettingSerializer(serializers.ModelSerializer):
    """
    Serializer for notification settings
    """
    class Meta:
        model = NotificationSetting
        fields = ['id', 'setting_type', 'value', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class NotificationTemplateSerializer(serializers.ModelSerializer):
    """
    Serializer for notification templates
    """
    class Meta:
        model = NotificationTemplate
        fields = ['id', 'type', 'subject_template', 'body_template', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class NotificationSettingsUpdateSerializer(serializers.Serializer):
    """
    Serializer for updating multiple notification settings at once
    """
    repayment_reminder_days = serializers.IntegerField(min_value=1, max_value=30, required=False)
    loan_expiration_days = serializers.IntegerField(min_value=1, max_value=90, required=False)
    late_repayment_days = serializers.IntegerField(min_value=1, max_value=30, required=False)
    stage_stagnation_days = serializers.IntegerField(min_value=1, max_value=30, required=False)
