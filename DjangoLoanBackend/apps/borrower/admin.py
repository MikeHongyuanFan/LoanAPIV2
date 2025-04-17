from django.contrib import admin
from .models import Borrower, BorrowerMergeRecord


@admin.register(Borrower)
class BorrowerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'date_of_birth', 'id_number']
    list_filter = ['gender', 'employment_status', 'created_at']
    search_fields = ['name', 'email', 'phone', 'id_number']
    readonly_fields = ['created_at', 'updated_at']
    
    actions = ['check_for_duplicates']
    
    def check_for_duplicates(self, request, queryset):
        """
        Admin action to check for potential duplicates of selected borrowers.
        """
        duplicate_count = 0
        message_parts = []
        
        for borrower in queryset:
            potential_duplicates = Borrower.find_potential_duplicates(borrower)
            if potential_duplicates.exists():
                duplicate_count += potential_duplicates.count()
                message_parts.append(f"{borrower.name}: {potential_duplicates.count()} potential duplicates")
        
        if duplicate_count > 0:
            self.message_user(request, f"Found {duplicate_count} potential duplicates. {', '.join(message_parts)}")
        else:
            self.message_user(request, "No potential duplicates found for selected borrowers.")
    
    check_for_duplicates.short_description = "Check for potential duplicates"


@admin.register(BorrowerMergeRecord)
class BorrowerMergeRecordAdmin(admin.ModelAdmin):
    list_display = ['primary_borrower', 'merged_borrower', 'merged_at', 'merged_by']
    list_filter = ['merged_at', 'merged_by']
    search_fields = ['primary_borrower__name', 'merged_borrower__name']
    readonly_fields = ['merged_at', 'merged_borrower_data']
