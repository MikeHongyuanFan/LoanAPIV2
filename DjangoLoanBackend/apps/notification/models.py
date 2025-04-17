from django.db import models
from django.utils import timezone


class NotificationTemplate(models.Model):
    TYPE_CHOICES = (
        ('STAGE_CHANGE', 'Stage Change'),
        ('STAGE_STAGNATION', 'Stage Stagnation'),
        ('NOTE_REMINDER', 'Note Reminder'),
        ('REPAYMENT_REMINDER', 'Repayment Reminder'),
        ('LATE_REPAYMENT', 'Late Repayment'),
        ('LATE_REPAYMENT_ADMIN', 'Late Repayment Admin'),
        ('LOAN_EXPIRATION', 'Loan Expiration'),
        ('EXTENSION_REQUEST', 'Extension Request'),
        ('EXTENSION_STATUS', 'Extension Status'),
        ('FEE_STATUS', 'Fee Status'),
    )
    
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    name = models.CharField(max_length=255)
    subject_template = models.CharField(max_length=255)
    body_template = models.TextField()
    variables = models.JSONField(default=dict)  # Store template variables
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class Notification(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('SENT', 'Sent'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled'),
    )
    
    type = models.CharField(max_length=50)
    recipient_email = models.EmailField(null=True, blank=True)
    recipient_phone = models.CharField(max_length=20, null=True, blank=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    error_message = models.TextField(null=True, blank=True)
    template = models.ForeignKey(NotificationTemplate, on_delete=models.SET_NULL, 
                                null=True, blank=True, related_name='notifications')
    created_by = models.ForeignKey('authentication.UserProfile', on_delete=models.SET_NULL, 
                                  null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    
    # Fields for tracking related entities and scheduling
    related_entity = models.CharField(max_length=50, null=True, blank=True)
    related_id = models.IntegerField(null=True, blank=True)
    trigger_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.type} to {self.recipient_email or self.recipient_phone}"
    
    def send(self):
        """
        Send the notification based on its type.
        """
        # This would be implemented with actual email/SMS sending logic
        # For now, just mark as sent
        self.status = 'SENT'
        self.sent_at = timezone.now()
        self.save()
        return True


class NotificationSetting(models.Model):
    SETTING_TYPE_CHOICES = (
        ('REPAYMENT_REMINDER_DAYS', 'Repayment Reminder Days'),
        ('LOAN_EXPIRATION_DAYS', 'Loan Expiration Days'),
        ('STAGE_STAGNATION_DAYS', 'Stage Stagnation Days'),
    )
    
    setting_type = models.CharField(max_length=50, choices=SETTING_TYPE_CHOICES, unique=True)
    value = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.get_setting_type_display()}: {self.value}"


class UserNotificationSetting(models.Model):
    user_profile = models.ForeignKey('authentication.UserProfile', on_delete=models.CASCADE, 
                                    related_name='notification_settings')
    notification_type = models.CharField(max_length=50)
    email_enabled = models.BooleanField(default=True)
    sms_enabled = models.BooleanField(default=False)
    system_enabled = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.notification_type} settings for {self.user_profile}"
