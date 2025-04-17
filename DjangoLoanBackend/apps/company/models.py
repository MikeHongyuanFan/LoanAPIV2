from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class Company(models.Model):
    """
    Model for company borrowers
    """
    COMPANY_TYPE_CHOICES = (
        ('PTY_LTD', 'Proprietary Limited (Pty Ltd)'),
        ('LTD', 'Limited (Ltd)'),
        ('TRUST', 'Trust'),
        ('PARTNERSHIP', 'Partnership'),
        ('SOLE_TRADER', 'Sole Trader'),
        ('INCORPORATED_ASSOCIATION', 'Incorporated Association'),
        ('OTHER', 'Other'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, help_text="Legal name of the company")
    trading_name = models.CharField(max_length=255, blank=True, null=True, help_text="Trading name if different from legal name")
    company_type = models.CharField(max_length=30, choices=COMPANY_TYPE_CHOICES, help_text="Type of company entity")
    
    # Registration information
    acn = models.CharField(max_length=9, blank=True, null=True, help_text="Australian Company Number")
    abn = models.CharField(max_length=11, blank=True, null=True, help_text="Australian Business Number")
    registration_date = models.DateField(help_text="Date the company was registered")
    registration_jurisdiction = models.CharField(max_length=50, help_text="Jurisdiction where the company is registered")
    
    # Address information
    registered_address_line1 = models.CharField(max_length=255, help_text="Registered address line 1")
    registered_address_line2 = models.CharField(max_length=255, blank=True, null=True, help_text="Registered address line 2")
    registered_city = models.CharField(max_length=100, help_text="Registered address city")
    registered_state = models.CharField(max_length=100, help_text="Registered address state/province")
    registered_postal_code = models.CharField(max_length=20, help_text="Registered address postal code")
    registered_country = models.CharField(max_length=100, default="Australia", help_text="Registered address country")
    
    business_address_line1 = models.CharField(max_length=255, help_text="Business address line 1")
    business_address_line2 = models.CharField(max_length=255, blank=True, null=True, help_text="Business address line 2")
    business_city = models.CharField(max_length=100, help_text="Business address city")
    business_state = models.CharField(max_length=100, help_text="Business address state/province")
    business_postal_code = models.CharField(max_length=20, help_text="Business address postal code")
    business_country = models.CharField(max_length=100, default="Australia", help_text="Business address country")
    
    # Contact information
    phone = models.CharField(max_length=20, help_text="Company phone number")
    email = models.EmailField(help_text="Company email address")
    website = models.URLField(blank=True, null=True, help_text="Company website")
    
    # Business information
    industry = models.CharField(max_length=100, help_text="Industry the company operates in")
    business_description = models.TextField(help_text="Brief description of the business")
    employees_count = models.PositiveIntegerField(default=0, help_text="Number of employees")
    years_in_business = models.PositiveIntegerField(default=0, help_text="Number of years in business")
    
    # System fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_registered_address(self):
        """
        Return the full registered address as a dictionary
        """
        return {
            'line1': self.registered_address_line1,
            'line2': self.registered_address_line2,
            'city': self.registered_city,
            'state': self.registered_state,
            'postal_code': self.registered_postal_code,
            'country': self.registered_country
        }
    
    def get_business_address(self):
        """
        Return the full business address as a dictionary
        """
        return {
            'line1': self.business_address_line1,
            'line2': self.business_address_line2,
            'city': self.business_city,
            'state': self.business_state,
            'postal_code': self.business_postal_code,
            'country': self.business_country
        }
    
    def get_directors_count(self):
        """
        Return the number of directors for this company
        """
        return self.directors.count()
    
    def get_shareholders_count(self):
        """
        Return the number of shareholders for this company
        """
        return self.shareholders.count()
    
    def get_latest_financial_year(self):
        """
        Return the most recent financial year information
        """
        return self.financials.order_by('-financial_year').first()


class Director(models.Model):
    """
    Model for company directors
    """
    ROLE_CHOICES = (
        ('MANAGING_DIRECTOR', 'Managing Director'),
        ('EXECUTIVE_DIRECTOR', 'Executive Director'),
        ('NON_EXECUTIVE_DIRECTOR', 'Non-Executive Director'),
        ('CHAIRPERSON', 'Chairperson'),
        ('COMPANY_SECRETARY', 'Company Secretary'),
        ('OTHER', 'Other'),
    )
    
    IDENTIFICATION_TYPE_CHOICES = (
        ('PASSPORT', 'Passport'),
        ('DRIVERS_LICENSE', 'Driver\'s License'),
        ('MEDICARE_CARD', 'Medicare Card'),
        ('OTHER', 'Other'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='directors')
    
    # Personal details
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    
    # Director information
    director_id = models.CharField(max_length=50, blank=True, null=True, help_text="Director identification number")
    appointment_date = models.DateField(help_text="Date appointed as director")
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='EXECUTIVE_DIRECTOR')
    
    # Address information
    residential_address_line1 = models.CharField(max_length=255)
    residential_address_line2 = models.CharField(max_length=255, blank=True, null=True)
    residential_city = models.CharField(max_length=100)
    residential_state = models.CharField(max_length=100)
    residential_postal_code = models.CharField(max_length=20)
    residential_country = models.CharField(max_length=100, default="Australia")
    
    # Contact information
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    
    # Identification
    identification_type = models.CharField(max_length=20, choices=IDENTIFICATION_TYPE_CHOICES)
    identification_number = models.CharField(max_length=50)
    identification_expiry = models.DateField(blank=True, null=True)
    
    # System fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Director"
        verbose_name_plural = "Directors"
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.company.name}"
    
    def get_full_name(self):
        """
        Return the director's full name
        """
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"
    
    def get_residential_address(self):
        """
        Return the full residential address as a dictionary
        """
        return {
            'line1': self.residential_address_line1,
            'line2': self.residential_address_line2,
            'city': self.residential_city,
            'state': self.residential_state,
            'postal_code': self.residential_postal_code,
            'country': self.residential_country
        }
    
    def is_shareholder(self):
        """
        Check if the director is also a shareholder
        """
        return self.shareholdings.exists()


class Shareholder(models.Model):
    """
    Model for company shareholders
    """
    SHAREHOLDER_TYPE_CHOICES = (
        ('INDIVIDUAL', 'Individual'),
        ('CORPORATE', 'Corporate'),
        ('TRUST', 'Trust'),
    )
    
    SHARE_CLASS_CHOICES = (
        ('ORDINARY', 'Ordinary Shares'),
        ('PREFERENCE', 'Preference Shares'),
        ('REDEEMABLE', 'Redeemable Shares'),
        ('OTHER', 'Other'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='shareholders')
    shareholder_type = models.CharField(max_length=20, choices=SHAREHOLDER_TYPE_CHOICES)
    
    # Individual shareholder details (if shareholder_type is INDIVIDUAL)
    individual_first_name = models.CharField(max_length=100, blank=True, null=True)
    individual_last_name = models.CharField(max_length=100, blank=True, null=True)
    individual_date_of_birth = models.DateField(blank=True, null=True)
    
    # Corporate shareholder details (if shareholder_type is CORPORATE)
    corporate_name = models.CharField(max_length=255, blank=True, null=True)
    corporate_acn = models.CharField(max_length=9, blank=True, null=True)
    corporate_abn = models.CharField(max_length=11, blank=True, null=True)
    
    # Trust shareholder details (if shareholder_type is TRUST)
    trust_name = models.CharField(max_length=255, blank=True, null=True)
    trust_abn = models.CharField(max_length=11, blank=True, null=True)
    trust_type = models.CharField(max_length=100, blank=True, null=True)
    
    # Shareholding details
    shareholding_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Percentage of shares owned"
    )
    share_class = models.CharField(max_length=20, choices=SHARE_CLASS_CHOICES, default='ORDINARY')
    acquisition_date = models.DateField(help_text="Date shares were acquired")
    
    # Director relationship (if shareholder is also a director)
    is_director = models.BooleanField(default=False, help_text="Whether the shareholder is also a director")
    director = models.ForeignKey(
        Director, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True, 
        related_name='shareholdings',
        help_text="Link to director record if shareholder is also a director"
    )
    
    # System fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Shareholder"
        verbose_name_plural = "Shareholders"
        ordering = ['-shareholding_percentage']
    
    def __str__(self):
        if self.shareholder_type == 'INDIVIDUAL':
            return f"{self.individual_first_name} {self.individual_last_name} - {self.shareholding_percentage}% of {self.company.name}"
        elif self.shareholder_type == 'CORPORATE':
            return f"{self.corporate_name} - {self.shareholding_percentage}% of {self.company.name}"
        else:  # TRUST
            return f"{self.trust_name} - {self.shareholding_percentage}% of {self.company.name}"
    
    def get_shareholder_name(self):
        """
        Return the name of the shareholder based on type
        """
        if self.shareholder_type == 'INDIVIDUAL':
            return f"{self.individual_first_name} {self.individual_last_name}"
        elif self.shareholder_type == 'CORPORATE':
            return self.corporate_name
        else:  # TRUST
            return self.trust_name
    
    def clean(self):
        """
        Validate the shareholder data based on shareholder_type
        """
        from django.core.exceptions import ValidationError
        
        if self.shareholder_type == 'INDIVIDUAL':
            if not self.individual_first_name or not self.individual_last_name or not self.individual_date_of_birth:
                raise ValidationError("Individual shareholder must have first name, last name, and date of birth")
        elif self.shareholder_type == 'CORPORATE':
            if not self.corporate_name:
                raise ValidationError("Corporate shareholder must have a company name")
        elif self.shareholder_type == 'TRUST':
            if not self.trust_name:
                raise ValidationError("Trust shareholder must have a trust name")
        
        if self.is_director and not self.director:
            raise ValidationError("If shareholder is a director, director field must be set")
        
        if self.director and self.shareholder_type != 'INDIVIDUAL':
            raise ValidationError("Only individual shareholders can be directors")


class FinancialInformation(models.Model):
    """
    Model for company financial information
    """
    SOURCE_CHOICES = (
        ('AUDITED', 'Audited Financial Statements'),
        ('MANAGEMENT', 'Management Accounts'),
        ('TAX_RETURN', 'Tax Return'),
        ('ACCOUNTANT_PREPARED', 'Accountant Prepared'),
        ('OTHER', 'Other'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='financials')
    
    # Financial year information
    financial_year = models.CharField(max_length=4, help_text="Financial year (YYYY)")
    financial_year_end_date = models.DateField(help_text="End date of the financial year")
    
    # Financial figures
    annual_revenue = models.DecimalField(max_digits=15, decimal_places=2, help_text="Annual revenue")
    annual_profit = models.DecimalField(max_digits=15, decimal_places=2, help_text="Annual profit/loss")
    total_assets = models.DecimalField(max_digits=15, decimal_places=2, help_text="Total assets")
    total_liabilities = models.DecimalField(max_digits=15, decimal_places=2, help_text="Total liabilities")
    current_assets = models.DecimalField(max_digits=15, decimal_places=2, help_text="Current assets")
    current_liabilities = models.DecimalField(max_digits=15, decimal_places=2, help_text="Current liabilities")
    equity = models.DecimalField(max_digits=15, decimal_places=2, help_text="Total equity")
    ebitda = models.DecimalField(max_digits=15, decimal_places=2, help_text="Earnings Before Interest, Taxes, Depreciation, and Amortization")
    
    # Source information
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, help_text="Source of financial information")
    notes = models.TextField(blank=True, null=True, help_text="Additional notes about the financial information")
    
    # System fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Financial Information"
        verbose_name_plural = "Financial Information"
        ordering = ['-financial_year', '-financial_year_end_date']
        unique_together = ['company', 'financial_year']
    
    def __str__(self):
        return f"{self.company.name} - Financial Year {self.financial_year}"
    
    def get_current_ratio(self):
        """
        Calculate the current ratio (current assets / current liabilities)
        """
        if self.current_liabilities == 0:
            return None
        return self.current_assets / self.current_liabilities
    
    def get_debt_to_equity_ratio(self):
        """
        Calculate the debt-to-equity ratio (total liabilities / equity)
        """
        if self.equity == 0:
            return None
        return self.total_liabilities / self.equity
    
    def get_profit_margin(self):
        """
        Calculate the profit margin (annual profit / annual revenue)
        """
        if self.annual_revenue == 0:
            return None
        return self.annual_profit / self.annual_revenue
