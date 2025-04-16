import uuid
from django.db import models
from django.utils import timezone

class Guarantor(models.Model):
    """
    Guarantor information model
    """
    TYPE_CHOICES = [
        ('INDIVIDUAL', 'Individual'),
        ('COMPANY', 'Company'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    name = models.CharField(max_length=255)
    borrower = models.ForeignKey('borrower.Borrower', on_delete=models.CASCADE, related_name='guarantors')
    application = models.ForeignKey('application.Application', on_delete=models.CASCADE, related_name='guarantors')
    created_at = models.DateTimeField(default=timezone.now)
    
    # Fields for individual guarantors
    dob = models.DateField(null=True, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    
    # Fields for company guarantors
    company_name = models.CharField(max_length=255, blank=True)
    abn = models.CharField(max_length=20, blank=True)
    acn = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"
