from django.db import models
from django.utils import timezone


class BrokerTier(models.Model):
    """
    Model for broker tiers (e.g., Gold, Silver, Bronze)
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    commission_multiplier = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class BrokerSpecialization(models.Model):
    """
    Model for broker specializations (e.g., Residential, Commercial, etc.)
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class Broker(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    company = models.CharField(max_length=255)
    address = models.TextField()
    license_number = models.CharField(max_length=50)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # New fields for Milestone 2.3
    branch = models.ForeignKey('branch.Branch', on_delete=models.SET_NULL, null=True, blank=True, related_name='brokers')
    bd = models.ForeignKey('bd.BD', on_delete=models.SET_NULL, null=True, blank=True, related_name='brokers')
    tier = models.ForeignKey(BrokerTier, on_delete=models.SET_NULL, null=True, blank=True, related_name='brokers')
    specializations = models.ManyToManyField(BrokerSpecialization, blank=True, related_name='brokers')
    
    # Additional broker information
    years_of_experience = models.PositiveIntegerField(default=0)
    accreditation_number = models.CharField(max_length=100, blank=True, null=True)
    accreditation_expiry = models.DateField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='broker_profiles/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    linkedin_profile = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} ({self.company})"
    
    def get_branch_name(self):
        """
        Return the name of the branch this broker belongs to
        """
        return self.branch.name if self.branch else None
    
    def get_bd_name(self):
        """
        Return the name of the BD this broker is associated with
        """
        return self.bd.get_full_name() if self.bd else None
    
    def get_tier_name(self):
        """
        Return the name of the broker's tier
        """
        return self.tier.name if self.tier else None
    
    def get_specialization_names(self):
        """
        Return a list of specialization names for this broker
        """
        return [spec.name for spec in self.specializations.all()]
    
    def is_accreditation_valid(self):
        """
        Check if the broker's accreditation is valid
        """
        if not self.accreditation_expiry:
            return False
        return self.accreditation_expiry >= timezone.now().date()


class BrokerCommission(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('CANCELLED', 'Cancelled'),
    )
    
    broker = models.ForeignKey(Broker, on_delete=models.CASCADE, related_name='commissions')
    application = models.ForeignKey('application.Application', on_delete=models.CASCADE, related_name='commissions')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Additional fields for payment tracking
    payment_date = models.DateField(null=True, blank=True)
    payment_reference = models.CharField(max_length=100, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"Commission for {self.broker.name} - {self.application.reference_number}"


class CommissionPayment(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('BANK_TRANSFER', 'Bank Transfer'),
        ('CHECK', 'Check'),
        ('CREDIT_CARD', 'Credit Card'),
        ('OTHER', 'Other'),
    )
    
    broker = models.ForeignKey(Broker, on_delete=models.CASCADE, related_name='payments')
    payment_date = models.DateField()
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='BANK_TRANSFER')
    reference_number = models.CharField(max_length=100)
    notes = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey('authentication.UserProfile', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Payment {self.reference_number} to {self.broker.name} on {self.payment_date}"


class CommissionPaymentItem(models.Model):
    payment = models.ForeignKey(CommissionPayment, on_delete=models.CASCADE, related_name='items')
    commission = models.ForeignKey(BrokerCommission, on_delete=models.CASCADE, related_name='payment_items')
    amount_paid = models.DecimalField(max_digits=15, decimal_places=2)
    
    def __str__(self):
        return f"Payment item for {self.commission}"
