from django.db import models
from django.utils import timezone
import os

class DocuSignIntegration(models.Model):
    """
    DocuSign integration settings
    """
    api_key = models.CharField(max_length=255, blank=True)
    api_secret = models.CharField(max_length=255, blank=True)
    integration_key = models.CharField(max_length=255, blank=True)
    user_id = models.CharField(max_length=255, blank=True)
    account_id = models.CharField(max_length=255, blank=True)
    base_url = models.CharField(max_length=255, default='https://demo.docusign.net/restapi')
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"DocuSign Integration ({self.base_url})"


def document_upload_path(instance, filename):
    """
    Define the upload path for documents.
    """
    # Get the application reference number or use 'general' if not linked to an application
    app_ref = instance.application.reference_number if instance.application else 'general'
    
    # Format: documents/APP-202504-ABC123/document_type/filename
    return f'documents/{app_ref}/{instance.document_type}/{filename}'


class DocumentTemplate(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    template_file = models.FileField(upload_to='templates/')
    document_type = models.CharField(max_length=100)
    variables = models.JSONField(default=dict)  # Store template variables
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class Document(models.Model):
    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('FINAL', 'Final'),
        ('SIGNED', 'Signed'),
        ('ARCHIVED', 'Archived'),
    )
    
    application = models.ForeignKey('application.Application', on_delete=models.CASCADE, 
                                   related_name='documents', null=True, blank=True)
    document_type = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to=document_upload_path)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    template = models.ForeignKey(DocumentTemplate, on_delete=models.SET_NULL, 
                                null=True, blank=True, related_name='generated_documents')
    original_document = models.ForeignKey('self', on_delete=models.SET_NULL, 
                                        null=True, blank=True, related_name='versions')
    version_number = models.IntegerField(default=1)
    created_by = models.ForeignKey('authentication.UserProfile', on_delete=models.SET_NULL, 
                                  null=True, blank=True, related_name='created_documents')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def filename(self):
        return os.path.basename(self.file.name)
    
    def file_extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension
    
    def create_new_version(self, new_file, created_by=None):
        """
        Create a new version of this document.
        """
        # If this is already a version, use the original document
        original = self.original_document if self.original_document else self
        
        # Get the highest version number
        highest_version = Document.objects.filter(
            original_document=original
        ).order_by('-version_number').first()
        
        new_version_number = highest_version.version_number + 1 if highest_version else 2
        
        # Create new version
        new_version = Document.objects.create(
            application=original.application,
            document_type=original.document_type,
            title=original.title,
            description=original.description,
            file=new_file,
            status='DRAFT',
            template=original.template,
            original_document=original,
            version_number=new_version_number,
            created_by=created_by
        )
        
        return new_version


class DocumentSigningRequest(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('SENT', 'Sent'),
        ('COMPLETED', 'Completed'),
        ('DECLINED', 'Declined'),
        ('EXPIRED', 'Expired'),
        ('CANCELLED', 'Cancelled'),
    )
    
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='signing_requests')
    recipient_name = models.CharField(max_length=255)
    recipient_email = models.EmailField()
    message = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    docusign_envelope_id = models.CharField(max_length=100, null=True, blank=True)
    created_by = models.ForeignKey('authentication.UserProfile', on_delete=models.SET_NULL, 
                                  null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Signing request for {self.document.title} to {self.recipient_name}"
    
    def mark_as_completed(self):
        """
        Mark the signing request as completed and update the document status.
        """
        self.status = 'COMPLETED'
        self.completed_at = timezone.now()
        self.save()
        
        # Update document status
        self.document.status = 'SIGNED'
        self.document.save()
