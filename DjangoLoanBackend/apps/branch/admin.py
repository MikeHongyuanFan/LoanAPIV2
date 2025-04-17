from django.contrib import admin
from .models import Branch


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'city', 'state', 'is_active', 'manager_name', 'created_at')
    list_filter = ('is_active', 'state', 'country')
    search_fields = ('name', 'code', 'city', 'manager_name')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Branch Information', {
            'fields': ('name', 'code', 'is_active')
        }),
        ('Address', {
            'fields': ('address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email')
        }),
        ('Manager Information', {
            'fields': ('manager_name', 'manager_email', 'manager_phone')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
