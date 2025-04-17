from django.db import models
import uuid


class BD(models.Model):
    """
    Business Development (BD) model representing a BD staff member
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    
    # Branch relationship
    branch = models.ForeignKey('branch.Branch', on_delete=models.PROTECT, related_name='bd_set')
    
    # Employment details
    employee_id = models.CharField(max_length=50, unique=True)
    position = models.CharField(max_length=100)
    hire_date = models.DateField()
    is_active = models.BooleanField(default=True)
    
    # Optional fields
    bio = models.TextField(blank=True, null=True)
    linkedin_profile = models.URLField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='bd_profiles/', blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'BD'
        verbose_name_plural = 'BDs'
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_full_name(self):
        """
        Return the full name of the BD
        """
        return f"{self.first_name} {self.last_name}"
    
    def get_branch_name(self):
        """
        Return the name of the branch this BD belongs to
        """
        return self.branch.name
    
    def get_experience_years(self):
        """
        Return the number of years of experience based on hire date
        """
        from django.utils import timezone
        from dateutil.relativedelta import relativedelta
        
        delta = relativedelta(timezone.now().date(), self.hire_date)
        return delta.years
