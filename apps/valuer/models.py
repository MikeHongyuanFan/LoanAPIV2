import uuid
from django.db import models
from django.utils import timezone

class Valuer(models.Model):
    """
    Valuer information model
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Additional fields
    address = models.TextField(blank=True)
    license_number = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.company})"
