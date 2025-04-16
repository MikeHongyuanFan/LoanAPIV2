import uuid
from django.db import models
from django.utils import timezone

class Product(models.Model):
    """
    Loan product information model
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Additional fields
    min_loan_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    max_loan_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    min_term = models.IntegerField(help_text="Minimum term in months", null=True, blank=True)
    max_term = models.IntegerField(help_text="Maximum term in months", null=True, blank=True)
    establishment_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
