from django.db import models
from django.utils import timezone
from django.conf import settings
import uuid


class Application(models.Model):
    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('SUBMITTED', 'Submitted'),
        ('PROCESSING', 'Processing'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('CANCELLED', 'Cancelled'),
        ('SETTLED', 'Settled'),
        ('CLOSED', 'Closed'),
    )
    
    STAGE_CHOICES = (
        ('INQUIRY', 'Inquiry'),
        ('APPLICATION', 'Application'),
        ('PROCESSING', 'Processing'),
        ('UNDERWRITING', 'Underwriting'),
        ('APPROVAL', 'Approval'),
        ('SETTLEMENT', 'Settlement'),
    )
    
    LOAN_TYPE_CHOICES = (
        ('RESIDENTIAL', 'Residential'),
        ('COMMERCIAL', 'Commercial'),
        ('CONSTRUCTION', 'Construction'),
        ('BRIDGING', 'Bridging'),
        ('REFINANCE', 'Refinance'),
    )
    
    reference_number = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default='INQUIRY')
    loan_type = models.CharField(max_length=20, choices=LOAN_TYPE_CHOICES)
    loan_amount = models.DecimalField(max_digits=15, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    term_months = models.IntegerField()
    property_address = models.TextField()
    property_value = models.DecimalField(max_digits=15, decimal_places=2)
    loan_purpose = models.TextField()
    
    # Relationships
    borrower = models.ForeignKey('borrower.Borrower', on_delete=models.CASCADE, related_name='applications')
    broker = models.ForeignKey('broker.Broker', on_delete=models.SET_NULL, null=True, blank=True, related_name='applications')
    valuer = models.ForeignKey('valuer.Valuer', on_delete=models.SET_NULL, null=True, blank=True, related_name='applications')
    qs = models.ForeignKey('qs.QS', on_delete=models.SET_NULL, null=True, blank=True, related_name='applications')
    product = models.ForeignKey('product.Product', on_delete=models.SET_NULL, null=True, blank=True, related_name='applications')
    assigned_to = models.ForeignKey('authentication.UserProfile', on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_applications')
    created_by = models.ForeignKey('authentication.UserProfile', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_applications')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.reference_number} - {self.borrower.name if self.borrower else 'No Borrower'}"
    
    def save(self, *args, **kwargs):
        if not self.reference_number:
            # Generate a unique reference number
            year = timezone.now().year
            month = timezone.now().month
            random_part = uuid.uuid4().hex[:6].upper()
            self.reference_number = f"APP-{year}{month:02d}-{random_part}"
        super().save(*args, **kwargs)


class Note(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='notes')
    content = models.TextField()
    created_by = models.ForeignKey('authentication.UserProfile', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    remind_date = models.DateField(null=True, blank=True)
    reminder_sent = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Note for {self.application.reference_number} - {self.created_at.strftime('%Y-%m-%d')}"


class Repayment(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('OVERDUE', 'Overdue'),
        ('CANCELLED', 'Cancelled'),
    )
    
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='repayments')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    payment_date = models.DateField(null=True, blank=True)
    payment_reference = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Repayment for {self.application.reference_number} - {self.due_date}"


class Extension(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='extensions')
    previous_term_months = models.IntegerField()
    new_term_months = models.IntegerField()
    previous_interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    new_interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    extension_fee = models.DecimalField(max_digits=15, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    approved_by = models.ForeignKey('authentication.UserProfile', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Extension for {self.application.reference_number} - {self.start_date} to {self.end_date}"


class Fee(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('WAIVED', 'Waived'),
    )
    
    TYPE_CHOICES = (
        ('APPLICATION', 'Application Fee'),
        ('VALUATION', 'Valuation Fee'),
        ('LEGAL', 'Legal Fee'),
        ('ESTABLISHMENT', 'Establishment Fee'),
        ('EXTENSION', 'Extension Fee'),
        ('OTHER', 'Other Fee'),
    )
    
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='fees')
    fee_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    description = models.TextField(null=True, blank=True)
    invoice_number = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.get_fee_type_display()} for {self.application.reference_number} - {self.amount}"


class Payment(models.Model):
    METHOD_CHOICES = (
        ('BANK_TRANSFER', 'Bank Transfer'),
        ('CREDIT_CARD', 'Credit Card'),
        ('DEBIT_CARD', 'Debit Card'),
        ('CASH', 'Cash'),
        ('CHEQUE', 'Cheque'),
        ('OTHER', 'Other'),
    )
    
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='payments')
    fee = models.ForeignKey(Fee, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    reference_number = models.CharField(max_length=100, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey('authentication.UserProfile', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payment for {self.application.reference_number} - {self.amount} on {self.payment_date}"
