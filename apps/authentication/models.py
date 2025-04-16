from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    """
    Extended user profile for the loan application system.
    """
    ROLE_CHOICES = [
        ('ADMIN', 'Administrator'),
        ('MANAGER', 'Manager'),
        ('STAFF', 'Staff'),
        ('BROKER', 'Broker'),
        ('READONLY', 'Read Only'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='STAFF')
    phone = models.CharField(max_length=20, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"


class Permission(models.Model):
    """
    Custom permission model for fine-grained access control.
    """
    RESOURCE_CHOICES = [
        ('APPLICATION', 'Application'),
        ('BORROWER', 'Borrower'),
        ('GUARANTOR', 'Guarantor'),
        ('BROKER', 'Broker'),
        ('VALUER', 'Valuer'),
        ('QS', 'Quantity Surveyor'),
        ('PRODUCT', 'Product'),
        ('DOCUMENT', 'Document'),
        ('NOTIFICATION', 'Notification'),
        ('USER', 'User'),
        ('REPORT', 'Report'),
    ]
    
    ACTION_CHOICES = [
        ('VIEW', 'View'),
        ('CREATE', 'Create'),
        ('EDIT', 'Edit'),
        ('DELETE', 'Delete'),
        ('APPROVE', 'Approve'),
        ('REJECT', 'Reject'),
        ('EXPORT', 'Export'),
        ('IMPORT', 'Import'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    resource = models.CharField(max_length=20, choices=RESOURCE_CHOICES)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.get_action_display()} {self.get_resource_display()}"


class Role(models.Model):
    """
    Custom role model for grouping permissions.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    permissions = models.ManyToManyField(Permission, related_name='roles')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class UserPermission(models.Model):
    """
    Model for assigning specific permissions to users.
    """
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_permissions')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    granted = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'permission')
    
    def __str__(self):
        action = "Granted" if self.granted else "Denied"
        return f"{action} {self.permission} to {self.user}"


class AuditLog(models.Model):
    """
    Model for tracking user actions for auditing purposes.
    """
    ACTION_CHOICES = [
        ('CREATE', 'Create'),
        ('READ', 'Read'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
        ('LOGIN', 'Login'),
        ('LOGOUT', 'Logout'),
        ('EXPORT', 'Export'),
        ('IMPORT', 'Import'),
        ('APPROVE', 'Approve'),
        ('REJECT', 'Reject'),
    ]
    
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, related_name='audit_logs')
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    resource_type = models.CharField(max_length=100)
    resource_id = models.CharField(max_length=100, blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user} {self.get_action_display()} {self.resource_type} at {self.timestamp}"
    
    class Meta:
        ordering = ['-timestamp']
