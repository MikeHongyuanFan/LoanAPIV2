from django.db import models
from django.utils import timezone
import uuid


class Application(models.Model):
    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('SUBMITTED', 'Submitted'),
        ('UNDER_REVIEW', 'Under Review'),
        ('PENDING_VALUATION', 'Pending Valuation'),
        ('PENDING_QS', 'Pending QS'),
        ('APPROVED', 'Approved'),
        ('CONDITIONALLY_APPROVED', 'Conditionally Approved'),
        ('DECLINED', 'Declined'),
        ('WITHDRAWN', 'Withdrawn'),
        ('SETTLED', 'Settled'),
        ('CLOSED', 'Closed'),
    )
    
    LOAN_PURPOSE_CHOICES = (
        ('PURCHASE', 'Purchase'),
        ('REFINANCE', 'Refinance'),
        ('CONSTRUCTION', 'Construction'),
        ('INVESTMENT', 'Investment'),
        ('BUSINESS', 'Business'),
        ('OTHER', 'Other'),
    )
    
    # Basic information
    reference_number = models.CharField(max_length=20, unique=True, editable=False)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='DRAFT')
    loan_amount = models.DecimalField(max_digits=15, decimal_places=2)
    loan_term_months = models.IntegerField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    loan_purpose = models.CharField(max_length=20, choices=LOAN_PURPOSE_CHOICES)
    
    # Relationships
    borrower = models.ForeignKey('borrower.Borrower', on_delete=models.PROTECT, related_name='applications')
    broker = models.ForeignKey('broker.Broker', on_delete=models.SET_NULL, null=True, blank=True, related_name='applications')
    valuer = models.ForeignKey('valuer.Valuer', on_delete=models.SET_NULL, null=True, blank=True, related_name='applications')
    qs = models.ForeignKey('qs.QS', on_delete=models.SET_NULL, null=True, blank=True, related_name='applications')
    product = models.ForeignKey('product.Product', on_delete=models.PROTECT, related_name='applications')
    
    # Property information
    property_address = models.TextField()
    property_type = models.CharField(max_length=50)
    property_value = models.DecimalField(max_digits=15, decimal_places=2)
    
    # Dates
    application_date = models.DateField(default=timezone.now)
    settlement_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    
    # User assignments
    assigned_to = models.ForeignKey('authentication.UserProfile', on_delete=models.SET_NULL, 
                                   null=True, blank=True, related_name='assigned_applications')
    created_by = models.ForeignKey('authentication.UserProfile', on_delete=models.SET_NULL, 
                                  null=True, blank=True, related_name='created_applications')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.reference_number} - {self.borrower.name}"
    
    def save(self, *args, **kwargs):
        # Generate reference number if not set
        if not self.reference_number:
            year = timezone.now().strftime('%Y')
            month = timezone.now().strftime('%m')
            unique_id = str(uuid.uuid4())[:8].upper()
            self.reference_number = f"APP-{year}{month}-{unique_id}"
        
        super().save(*args, **kwargs)
    
    def get_loan_to_value_ratio(self):
        """
        Calculate the Loan-to-Value Ratio (LVR).
        """
        if self.property_value > 0:
            return (self.loan_amount / self.property_value) * 100
        return 0
    
    def is_expired(self):
        """
        Check if the loan has expired.
        """
        if self.expiry_date:
            return self.expiry_date < timezone.now().date()
        return False


class Note(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='notes')
    content = models.TextField()
    created_by = models.ForeignKey('authentication.UserProfile', on_delete=models.SET_NULL, 
                                  null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Reminder fields
    has_reminder = models.BooleanField(default=False)
    reminder_date = models.DateTimeField(null=True, blank=True)
    reminder_sent = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Note for {self.application.reference_number} at {self.created_at}"


class Repayment(models.Model):
    STATUS_CHOICES = (
        ('SCHEDULED', 'Scheduled'),
        ('PAID', 'Paid'),
        ('OVERDUE', 'Overdue'),
        ('PARTIAL', 'Partially Paid'),
        ('WAIVED', 'Waived'),
    )
    
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='repayments')
    due_date = models.DateField()
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    principal_amount = models.DecimalField(max_digits=15, decimal_places=2)
    interest_amount = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SCHEDULED')
    paid_date = models.DateField(null=True, blank=True)
    paid_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    def __str__(self):
        return f"Repayment for {self.application.reference_number} due on {self.due_date}"
    
    def is_overdue(self):
        """
        Check if the repayment is overdue.
        """
        return self.status != 'PAID' and self.due_date < timezone.now().date()


class Extension(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('DECLINED', 'Declined'),
    )
    
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='extensions')
    requested_date = models.DateField(default=timezone.now)
    original_expiry_date = models.DateField()
    new_expiry_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    approved_by = models.ForeignKey('authentication.UserProfile', on_delete=models.SET_NULL, 
                                   null=True, blank=True, related_name='approved_extensions')
    created_by = models.ForeignKey('authentication.UserProfile', on_delete=models.SET_NULL, 
                                  null=True, blank=True, related_name='created_extensions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Extension for {self.application.reference_number} to {self.new_expiry_date}"


class Fee(models.Model):
    TYPE_CHOICES = (
        ('ESTABLISHMENT', 'Establishment Fee'),
        ('VALUATION', 'Valuation Fee'),
        ('LEGAL', 'Legal Fee'),
        ('PROCESSING', 'Processing Fee'),
        ('LATE_PAYMENT', 'Late Payment Fee'),
        ('OTHER', 'Other Fee'),
    )
    
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('WAIVED', 'Waived'),
    )
    
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='fees')
    fee_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.get_fee_type_display()} for {self.application.reference_number}"


class Payment(models.Model):
    METHOD_CHOICES = (
        ('BANK_TRANSFER', 'Bank Transfer'),
        ('CREDIT_CARD', 'Credit Card'),
        ('DIRECT_DEBIT', 'Direct Debit'),
        ('CASH', 'Cash'),
        ('CHECK', 'Check'),
        ('OTHER', 'Other'),
    )
    
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    reference = models.CharField(max_length=100, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey('authentication.UserProfile', on_delete=models.SET_NULL, 
                                  null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payment of {self.amount} for {self.application.reference_number}"
