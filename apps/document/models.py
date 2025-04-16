import uuid
import os
from django.db import models
from django.utils import timezone

def document_upload_path(instance, filename):
    """Generate file path for document uploads"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('documents', str(instance.application.id), filename)

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
