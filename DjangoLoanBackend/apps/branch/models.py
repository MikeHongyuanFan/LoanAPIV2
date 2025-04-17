from django.db import models
import uuid


class Branch(models.Model):
    """
    Branch model representing a physical branch office location
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='Australia')
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    
    # Manager information
    manager_name = models.CharField(max_length=255, blank=True, null=True)
    manager_email = models.EmailField(blank=True, null=True)
    manager_phone = models.CharField(max_length=20, blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Branch'
        verbose_name_plural = 'Branches'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    def get_full_address(self):
        """
        Return the full address as a formatted string
        """
        address_parts = [self.address_line1]
        
        if self.address_line2:
            address_parts.append(self.address_line2)
            
        address_parts.append(f"{self.city}, {self.state} {self.postal_code}")
        address_parts.append(self.country)
        
        return "\n".join(address_parts)
    
    def get_bd_count(self):
        """
        Return the number of BDs associated with this branch
        """
        return self.bd_set.count()
    
    def get_active_bd_count(self):
        """
        Return the number of active BDs associated with this branch
        """
        return self.bd_set.filter(is_active=True).count()
