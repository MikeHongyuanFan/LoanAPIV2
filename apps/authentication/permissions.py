from rest_framework import permissions
from .models import UserProfile, Permission, UserPermission


class IsAdmin(permissions.BasePermission):
    """
    Permission check for administrators.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profile.role == 'ADMIN'


class IsManager(permissions.BasePermission):
    """
    Permission check for managers.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profile.role in ['ADMIN', 'MANAGER']


class IsStaff(permissions.BasePermission):
    """
    Permission check for staff members.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profile.role in ['ADMIN', 'MANAGER', 'STAFF']


class IsBroker(permissions.BasePermission):
    """
    Permission check for brokers.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profile.role == 'BROKER'


class IsReadOnly(permissions.BasePermission):
    """
    Permission check for read-only users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.method in permissions.SAFE_METHODS


class HasResourcePermission(permissions.BasePermission):
    """
    Permission check for specific resource and action.
    
    Usage:
        permission_classes = [HasResourcePermission('APPLICATION', 'VIEW')]
    """
    def __init__(self, resource, action):
        self.resource = resource
        self.action = action
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Admins have all permissions
        if request.user.profile.role == 'ADMIN':
            return True
        
        try:
            # Check if the user has the specific permission
            permission = Permission.objects.get(resource=self.resource, action=self.action)
            user_permission = UserPermission.objects.filter(
                user=request.user.profile,
                permission=permission
            ).first()
            
            # If explicit permission exists, return its granted status
            if user_permission:
                return user_permission.granted
            
            # Check if the user's role has the permission
            if hasattr(request.user.profile, 'role'):
                role_has_permission = request.user.profile.role.permissions.filter(
                    resource=self.resource,
                    action=self.action
                ).exists()
                
                if role_has_permission:
                    return True
            
            # Default permissions based on role
            if self.action == 'VIEW':
                return request.user.profile.role in ['MANAGER', 'STAFF', 'READONLY']
            elif self.action in ['CREATE', 'EDIT']:
                return request.user.profile.role in ['MANAGER', 'STAFF']
            elif self.action in ['DELETE', 'APPROVE', 'REJECT']:
                return request.user.profile.role == 'MANAGER'
            
            return False
        except Permission.DoesNotExist:
            # If permission doesn't exist in the system, deny access
            return False


class HasObjectPermission(permissions.BasePermission):
    """
    Permission check for specific object-level permissions.
    
    Usage:
        permission_classes = [HasObjectPermission('APPLICATION', 'EDIT')]
    """
    def __init__(self, resource, action):
        self.resource = resource
        self.action = action
    
    def has_object_permission(self, request, view, obj):
        # Admins have all permissions
        if request.user.profile.role == 'ADMIN':
            return True
        
        # Brokers can only access their own resources
        if request.user.profile.role == 'BROKER':
            # Check if the object has a broker field and it matches the user
            if hasattr(obj, 'broker') and hasattr(obj.broker, 'user'):
                return obj.broker.user == request.user
            return False
        
        # For other roles, use the same logic as HasResourcePermission
        try:
            permission = Permission.objects.get(resource=self.resource, action=self.action)
            user_permission = UserPermission.objects.filter(
                user=request.user.profile,
                permission=permission
            ).first()
            
            if user_permission:
                return user_permission.granted
            
            if hasattr(request.user.profile, 'role'):
                role_has_permission = request.user.profile.role.permissions.filter(
                    resource=self.resource,
                    action=self.action
                ).exists()
                
                if role_has_permission:
                    return True
            
            if self.action == 'VIEW':
                return request.user.profile.role in ['MANAGER', 'STAFF', 'READONLY']
            elif self.action in ['CREATE', 'EDIT']:
                return request.user.profile.role in ['MANAGER', 'STAFF']
            elif self.action in ['DELETE', 'APPROVE', 'REJECT']:
                return request.user.profile.role == 'MANAGER'
            
            return False
        except Permission.DoesNotExist:
            return False
