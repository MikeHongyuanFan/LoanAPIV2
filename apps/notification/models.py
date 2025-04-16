import uuid
from django.db import models
from django.utils import timezone

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
