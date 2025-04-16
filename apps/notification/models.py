import uuid
from django.db import models
from django.utils import timezone
from django.conf import settings

class NotificationSetting(models.Model):
    """
    Settings for notification triggers
    """
    SETTING_TYPE_CHOICES = [
        ('REPAYMENT_REMINDER_DAYS', 'Days before repayment to send reminder'),
        ('LOAN_EXPIRATION_DAYS', 'Days before loan expiration to send reminder'),
        ('LATE_REPAYMENT_DAYS', 'Days after repayment to send late notice'),
        ('STAGE_STAGNATION_DAYS', 'Days in same stage to trigger stagnation alert'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    setting_type = models.CharField(max_length=30, choices=SETTING_TYPE_CHOICES, unique=True)
    value = models.IntegerField(help_text="Value in days")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.get_setting_type_display()}: {self.value} days"

class Notification(models.Model):
    """
    Notification model for email and system notifications
    """
    TYPE_CHOICES = [
        ('REPAYMENT_REMINDER', 'Repayment Reminder'),
        ('LOAN_EXPIRATION', 'Loan Expiration'),
        ('LATE_REPAYMENT', 'Late Repayment'),
        ('STAGE_CHANGE', 'Stage Change'),
        ('STAGE_STAGNATION', 'Stage Stagnation'),
        ('DOCUMENT_UPLOAD', 'Document Upload'),
        ('NOTE_REMINDER', 'Note Reminder'),
        ('OTHER', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SENT', 'Sent'),
        ('FAILED', 'Failed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    recipient_email = models.EmailField()
    related_id = models.UUIDField(help_text="UUID of the related object (application, repayment, etc.)")
    trigger_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    
    # Additional fields
    subject = models.CharField(max_length=255)
    message = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    sent_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.get_type_display()} to {self.recipient_email}"
    
    def send(self):
        """
        Send the notification via email
        """
        try:
            # In a real implementation, this would use Django's email functionality
            # For now, we'll just mark it as sent
            self.status = 'SENT'
            self.sent_at = timezone.now()
            self.save()
            return True
        except Exception as e:
            self.status = 'FAILED'
            self.save()
            return False

class NotificationTemplate(models.Model):
    """
    Templates for different notification types
    """
    TYPE_CHOICES = [
        ('REPAYMENT_REMINDER', 'Repayment Reminder'),
        ('LOAN_EXPIRATION', 'Loan Expiration'),
        ('LATE_REPAYMENT', 'Late Repayment'),
        ('STAGE_CHANGE', 'Stage Change'),
        ('STAGE_STAGNATION', 'Stage Stagnation'),
        ('DOCUMENT_UPLOAD', 'Document Upload'),
        ('NOTE_REMINDER', 'Note Reminder'),
        ('OTHER', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, unique=True)
    subject_template = models.CharField(max_length=255)
    body_template = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Template for {self.get_type_display()}"
