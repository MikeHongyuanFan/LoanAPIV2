from rest_framework import permissions

class IsManager(permissions.BasePermission):
    """
    Custom permission to only allow managers to access the view.
    """
    def has_permission(self, request, view):
        # Check if user is authenticated and has manager role
        return request.user.is_authenticated and request.user.has_role('MANAGER')

class IsStaff(permissions.BasePermission):
    """
    Custom permission to only allow staff members to access the view.
    """
    def has_permission(self, request, view):
        # Check if user is authenticated and has staff role
        return request.user.is_authenticated and request.user.has_role('STAFF')

class IsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow admin users to access the view.
    """
    def has_permission(self, request, view):
        # Check if user is authenticated and has admin role
        return request.user.is_authenticated and request.user.has_role('ADMIN')

class HasObjectPermission(permissions.BasePermission):
    """
    Custom permission to check if user has specific permission for an object.
    """
    def has_object_permission(self, request, view, obj):
        # Check if user has permission for this object
        if hasattr(obj, 'has_permission'):
            return obj.has_permission(request.user, request.method)
        return False
