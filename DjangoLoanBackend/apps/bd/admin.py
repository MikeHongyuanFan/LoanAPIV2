from django.contrib import admin
from .models import BD


@admin.register(BD)
class BDAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'employee_id', 'position', 'get_branch_name', 'email', 'is_active', 'hire_date')
    list_filter = ('is_active', 'position', 'branch', 'hire_date')
    search_fields = ('first_name', 'last_name', 'email', 'employee_id')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'profile_image')
        }),
        ('Employment Details', {
            'fields': ('branch', 'employee_id', 'position', 'hire_date', 'is_active')
        }),
        ('Additional Information', {
            'fields': ('bio', 'linkedin_profile'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_branch_name(self, obj):
        return obj.get_branch_name()
    get_branch_name.short_description = 'Branch'
    get_branch_name.admin_order_field = 'branch__name'
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'Name'
    get_full_name.admin_order_field = 'last_name'
