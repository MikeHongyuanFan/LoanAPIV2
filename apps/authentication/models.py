from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    """
    Extended user profile model
    """
    ROLE_CHOICES = [
        ('ADMIN', 'Administrator'),
        ('MANAGER', 'Manager'),
        ('STAFF', 'Staff'),
        ('BROKER', 'Broker'),
        ('CLIENT', 'Client'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='STAFF')
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    # Additional fields
    broker = models.ForeignKey('broker.Broker', on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    borrower = models.ForeignKey('borrower.Borrower', on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    
    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"
