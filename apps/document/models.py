import uuid
import os
from django.db import models
from django.utils import timezone

def document_upload_path(instance, filename):
    """Generate file path for document uploads"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('documents', str(instance.application.id), filename)

def template_upload_path(instance, filename):
    """Generate file path for template uploads"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('templates', instance.type, filename)

class Document(models.Model):
    """
    Document model for storing application-related files
    """
    TYPE_CHOICES = [
        ('APPLICATION_FORM', 'Application Form'),
        ('DISBURSEMENT_LETTER', 'Disbursement Letter'),
        ('INDICATIVE_LETTER', 'Indicative Letter'),
        ('STATEMENT', 'Statement'),
        ('VALUATION', 'Valuation Report'),
        ('ID', 'Identification Document'),
        ('BANK_STATEMENT', 'Bank Statement'),
        ('OTHER', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application = models.ForeignKey('application.Application', on_delete=models.CASCADE, related_name='documents')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    file = models.FileField(upload_to=document_upload_path)
    created_at = models.DateTimeField(default=timezone.now)
    
    # Additional fields
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_signed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.get_type_display()} for {self.application.id}"
    
    @property
    def file_path(self):
        return self.file.path if self.file else None
    
    @property
    def file_url(self):
        return self.file.url if self.file else None

class DocumentTemplate(models.Model):
    """
    Document template model for generating documents
    """
    TYPE_CHOICES = [
        ('APPLICATION_FORM', 'Application Form'),
        ('DISBURSEMENT_LETTER', 'Disbursement Letter'),
        ('INDICATIVE_LETTER', 'Indicative Letter'),
        ('STATEMENT', 'Statement'),
        ('OTHER', 'Other'),
    ]
    
    RECIPIENT_CHOICES = [
        ('CLIENT', 'Client'),
        ('SOLICITOR', 'Solicitor'),
        ('INTERNAL', 'Internal'),
        ('BROKER', 'Broker'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    recipient_type = models.CharField(max_length=10, choices=RECIPIENT_CHOICES, default='CLIENT')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    template_file = models.FileField(upload_to=template_upload_path)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.get_type_display()} Template for {self.get_recipient_type_display()}"
    
    class Meta:
        unique_together = ('type', 'recipient_type')

class DocuSignIntegration(models.Model):
    """
    DocuSign integration settings
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    api_key = models.CharField(max_length=255)
    api_secret = models.CharField(max_length=255)
    integration_key = models.CharField(max_length=255)
    user_id = models.CharField(max_length=255)
    account_id = models.CharField(max_length=255)
    base_url = models.URLField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"DocuSign Integration ({self.user_id})"
    
    class Meta:
        verbose_name = "DocuSign Integration"
        verbose_name_plural = "DocuSign Integration"

class DocumentSigningRequest(models.Model):
    """
    Document signing request model
    """
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SENT', 'Sent'),
        ('COMPLETED', 'Completed'),
        ('DECLINED', 'Declined'),
        ('EXPIRED', 'Expired'),
        ('FAILED', 'Failed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='signing_requests')
    recipient_email = models.EmailField()
    recipient_name = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    docusign_envelope_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Signing Request for {self.document.name} to {self.recipient_email}"
