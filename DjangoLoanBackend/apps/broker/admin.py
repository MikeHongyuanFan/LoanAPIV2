from django.contrib import admin
from .models import Broker, BrokerCommission, CommissionPayment, CommissionPaymentItem, BrokerTier, BrokerSpecialization


@admin.register(BrokerTier)
class BrokerTierAdmin(admin.ModelAdmin):
    list_display = ('name', 'commission_multiplier', 'created_at')
    search_fields = ('name',)


@admin.register(BrokerSpecialization)
class BrokerSpecializationAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)


class BrokerCommissionInline(admin.TabularInline):
    model = BrokerCommission
    extra = 0
    fields = ('application', 'amount', 'status', 'payment_date')
    readonly_fields = ('application', 'amount')


@admin.register(Broker)
class BrokerAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'email', 'phone', 'get_branch_name', 'get_bd_name', 'get_tier_name', 'active')
    list_filter = ('active', 'branch', 'tier', 'specializations')
    search_fields = ('name', 'email', 'company', 'license_number')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('specializations',)
    inlines = [BrokerCommissionInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'email', 'phone', 'company', 'address', 'license_number', 'active')
        }),
        ('Branch and BD Information', {
            'fields': ('branch', 'bd')
        }),
        ('Categorization', {
            'fields': ('tier', 'specializations')
        }),
        ('Commission Information', {
            'fields': ('commission_rate',)
        }),
        ('Additional Information', {
            'fields': ('years_of_experience', 'accreditation_number', 'accreditation_expiry', 'profile_image', 'bio')
        }),
        ('Online Presence', {
            'fields': ('website', 'linkedin_profile'),
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
    
    def get_bd_name(self, obj):
        return obj.get_bd_name()
    get_bd_name.short_description = 'BD'
    get_bd_name.admin_order_field = 'bd__last_name'
    
    def get_tier_name(self, obj):
        return obj.get_tier_name()
    get_tier_name.short_description = 'Tier'
    get_tier_name.admin_order_field = 'tier__name'


class CommissionPaymentItemInline(admin.TabularInline):
    model = CommissionPaymentItem
    extra = 0
    fields = ('commission', 'amount_paid')
    readonly_fields = ('commission',)


@admin.register(BrokerCommission)
class BrokerCommissionAdmin(admin.ModelAdmin):
    list_display = ('broker', 'application', 'amount', 'status', 'payment_date')
    list_filter = ('status', 'payment_date')
    search_fields = ('broker__name', 'application__reference_number')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(CommissionPayment)
class CommissionPaymentAdmin(admin.ModelAdmin):
    list_display = ('broker', 'payment_date', 'total_amount', 'payment_method', 'reference_number')
    list_filter = ('payment_date', 'payment_method')
    search_fields = ('broker__name', 'reference_number')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [CommissionPaymentItemInline]
