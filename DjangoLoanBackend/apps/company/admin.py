from django.contrib import admin
from .models import Company, Director, Shareholder, FinancialInformation


class DirectorInline(admin.TabularInline):
    model = Director
    extra = 0
    fields = ('first_name', 'last_name', 'role', 'appointment_date', 'phone', 'email')


class ShareholderInline(admin.TabularInline):
    model = Shareholder
    extra = 0
    fields = ('get_shareholder_name', 'shareholder_type', 'shareholding_percentage', 'share_class', 'is_director')
    readonly_fields = ('get_shareholder_name',)


class FinancialInformationInline(admin.TabularInline):
    model = FinancialInformation
    extra = 0
    fields = ('financial_year', 'annual_revenue', 'annual_profit', 'total_assets', 'total_liabilities', 'source')


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'company_type', 'registration_date', 'get_directors_count', 'get_shareholders_count', 'phone', 'email')
    list_filter = ('company_type', 'registration_jurisdiction')
    search_fields = ('name', 'trading_name', 'acn', 'abn', 'email')
    date_hierarchy = 'registration_date'
    inlines = [DirectorInline, ShareholderInline, FinancialInformationInline]
    fieldsets = (
        ('Company Information', {
            'fields': ('name', 'trading_name', 'company_type', 'industry', 'business_description')
        }),
        ('Registration Details', {
            'fields': ('acn', 'abn', 'registration_date', 'registration_jurisdiction')
        }),
        ('Registered Address', {
            'fields': ('registered_address_line1', 'registered_address_line2', 'registered_city', 
                      'registered_state', 'registered_postal_code', 'registered_country')
        }),
        ('Business Address', {
            'fields': ('business_address_line1', 'business_address_line2', 'business_city', 
                      'business_state', 'business_postal_code', 'business_country')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'website')
        }),
        ('Business Details', {
            'fields': ('employees_count', 'years_in_business')
        }),
    )
    
    def get_directors_count(self, obj):
        return obj.get_directors_count()
    get_directors_count.short_description = 'Directors'
    
    def get_shareholders_count(self, obj):
        return obj.get_shareholders_count()
    get_shareholders_count.short_description = 'Shareholders'


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'company', 'role', 'appointment_date', 'phone', 'email', 'is_shareholder')
    list_filter = ('role', 'company')
    search_fields = ('first_name', 'last_name', 'company__name', 'email')
    date_hierarchy = 'appointment_date'
    fieldsets = (
        ('Company', {
            'fields': ('company',)
        }),
        ('Personal Details', {
            'fields': ('first_name', 'middle_name', 'last_name', 'date_of_birth')
        }),
        ('Director Information', {
            'fields': ('director_id', 'appointment_date', 'role')
        }),
        ('Residential Address', {
            'fields': ('residential_address_line1', 'residential_address_line2', 'residential_city', 
                      'residential_state', 'residential_postal_code', 'residential_country')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email')
        }),
        ('Identification', {
            'fields': ('identification_type', 'identification_number', 'identification_expiry')
        }),
    )


@admin.register(Shareholder)
class ShareholderAdmin(admin.ModelAdmin):
    list_display = ('get_shareholder_name', 'company', 'shareholder_type', 'shareholding_percentage', 'share_class', 'is_director')
    list_filter = ('shareholder_type', 'share_class', 'is_director', 'company')
    search_fields = ('individual_first_name', 'individual_last_name', 'corporate_name', 'trust_name', 'company__name')
    date_hierarchy = 'acquisition_date'
    fieldsets = (
        ('Company', {
            'fields': ('company',)
        }),
        ('Shareholder Type', {
            'fields': ('shareholder_type',)
        }),
        ('Individual Shareholder', {
            'fields': ('individual_first_name', 'individual_last_name', 'individual_date_of_birth'),
            'classes': ('individual_fields',)
        }),
        ('Corporate Shareholder', {
            'fields': ('corporate_name', 'corporate_acn', 'corporate_abn'),
            'classes': ('corporate_fields',)
        }),
        ('Trust Shareholder', {
            'fields': ('trust_name', 'trust_abn', 'trust_type'),
            'classes': ('trust_fields',)
        }),
        ('Shareholding Details', {
            'fields': ('shareholding_percentage', 'share_class', 'acquisition_date')
        }),
        ('Director Relationship', {
            'fields': ('is_director', 'director')
        }),
    )
    
    class Media:
        js = ('js/shareholder_admin.js',)


@admin.register(FinancialInformation)
class FinancialInformationAdmin(admin.ModelAdmin):
    list_display = ('company', 'financial_year', 'annual_revenue', 'annual_profit', 'get_current_ratio', 'get_debt_to_equity_ratio', 'source')
    list_filter = ('source', 'financial_year', 'company')
    search_fields = ('company__name', 'financial_year')
    date_hierarchy = 'financial_year_end_date'
    fieldsets = (
        ('Company', {
            'fields': ('company',)
        }),
        ('Financial Year', {
            'fields': ('financial_year', 'financial_year_end_date')
        }),
        ('Financial Figures', {
            'fields': ('annual_revenue', 'annual_profit', 'total_assets', 'total_liabilities', 
                      'current_assets', 'current_liabilities', 'equity', 'ebitda')
        }),
        ('Source Information', {
            'fields': ('source', 'notes')
        }),
    )
    
    def get_current_ratio(self, obj):
        ratio = obj.get_current_ratio()
        return f"{ratio:.2f}" if ratio is not None else "N/A"
    get_current_ratio.short_description = 'Current Ratio'
    
    def get_debt_to_equity_ratio(self, obj):
        ratio = obj.get_debt_to_equity_ratio()
        return f"{ratio:.2f}" if ratio is not None else "N/A"
    get_debt_to_equity_ratio.short_description = 'Debt/Equity'
