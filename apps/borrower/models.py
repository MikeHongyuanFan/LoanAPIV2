import uuid
from django.db import models
from django.utils import timezone

class Borrower(models.Model):
    """
    Borrower information model
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    dob = models.DateField(null=True, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Additional fields
    company_name = models.CharField(max_length=255, blank=True)
    abn = models.CharField(max_length=20, blank=True)
    acn = models.CharField(max_length=20, blank=True)
    broker = models.ForeignKey('broker.Broker', on_delete=models.SET_NULL, null=True, blank=True, related_name='borrowers')
    
    class Meta:
        unique_together = ['name', 'dob', 'email']
    
    def __str__(self):
        return self.name
