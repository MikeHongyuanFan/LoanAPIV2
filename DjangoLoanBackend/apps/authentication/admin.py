from django.contrib import admin
from .models import UserProfile, Permission, Role, UserPermission, AuditLog


class UserPermissionInline(admin.TabularInline):
    model = UserPermission
    extra = 0


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'department', 'created_at']
    list_filter = ['role', 'department', 'created_at']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name']
    inlines = [UserPermissionInline]


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'resource', 'action', 'description']
    list_filter = ['resource', 'action']
    search_fields = ['name', 'description']


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    filter_horizontal = ['permissions']
    search_fields = ['name', 'description']


@admin.register(UserPermission)
class UserPermissionAdmin(admin.ModelAdmin):
    list_display = ['user', 'permission', 'granted', 'created_at']
    list_filter = ['granted', 'created_at', 'permission__resource', 'permission__action']
    search_fields = ['user__user__username', 'permission__name']


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'resource_type', 'resource_id', 'timestamp']
    list_filter = ['action', 'resource_type', 'timestamp']
    search_fields = ['user__user__username', 'resource_id', 'ip_address']
    readonly_fields = ['user', 'action', 'resource_type', 'resource_id', 'details', 'ip_address', 'user_agent', 'timestamp']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
