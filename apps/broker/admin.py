from django.contrib import admin
from .models import Broker, BrokerCommission, CommissionPayment, CommissionPaymentItem


class BrokerCommissionInline(admin.TabularInline):
    model = BrokerCommission
    extra = 0
    readonly_fields = ['created_at', 'updated_at']


class CommissionPaymentItemInline(admin.TabularInline):
    model = CommissionPaymentItem
    extra = 0


@admin.register(Broker)
class BrokerAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'email', 'license_number', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'company', 'email', 'license_number']
    inlines = [BrokerCommissionInline]


@admin.register(BrokerCommission)
class BrokerCommissionAdmin(admin.ModelAdmin):
    list_display = ['broker', 'application', 'amount', 'percentage', 'status', 'payment_date']
    list_filter = ['status', 'payment_date', 'created_at']
    search_fields = ['broker__name', 'application__reference_number']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(CommissionPayment)
class CommissionPaymentAdmin(admin.ModelAdmin):
    list_display = ['broker', 'payment_date', 'total_amount', 'payment_method', 'reference_number']
    list_filter = ['payment_date', 'payment_method']
    search_fields = ['broker__name', 'reference_number']
    inlines = [CommissionPaymentItemInline]
    readonly_fields = ['created_at', 'updated_at']
