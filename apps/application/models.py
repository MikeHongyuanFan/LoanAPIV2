import uuid
import os
from django.db import models
from django.utils import timezone

def invoice_upload_path(instance, filename):
    """Generate file path for invoice uploads"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('invoices', str(instance.application.id), filename)

class Application(models.Model):
    """
    Core model for loan applications
    """
    STAGE_CHOICES = [
        ('INQUIRY', 'Inquiry'),
        ('APPLICATION', 'Application'),
        ('ASSESSMENT', 'Assessment'),
        ('VALUATION', 'Valuation'),
        ('APPROVAL', 'Approval'),
        ('SETTLEMENT', 'Settlement'),
        ('ACTIVE', 'Active'),
        ('CLOSED', 'Closed'),
        ('DECLINED', 'Declined'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    borrower = models.ForeignKey('borrower.Borrower', on_delete=models.CASCADE, related_name='applications')
    broker = models.ForeignKey('broker.Broker', on_delete=models.SET_NULL, null=True, blank=True, related_name='applications')
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default='INQUIRY')
    loan_amount = models.DecimalField(max_digits=15, decimal_places=2)
    product = models.ForeignKey('product.Product', on_delete=models.SET_NULL, null=True, related_name='applications')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Additional fields
    valuer = models.ForeignKey('valuer.Valuer', on_delete=models.SET_NULL, null=True, blank=True, related_name='applications')
    qs = models.ForeignKey('qs.QS', on_delete=models.SET_NULL, null=True, blank=True, related_name='applications')
    property_address = models.TextField(blank=True)
    loan_term = models.IntegerField(help_text="Loan term in months", null=True, blank=True)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    settlement_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"Application {self.id} - {self.borrower.name}"
        
    def duplicate(self):
        """
        Create a duplicate of this application with related data
        """
        # Create a new application with the same data but a new ID
        old_id = self.id
        self.id = uuid.uuid4()
        self.pk = None
        self.stage = 'INQUIRY'  # Reset stage for the new application
        self.created_at = timezone.now()
        self.updated_at = None
        self.settlement_date = None
        self.expiry_date = None
        self.save()
        
        new_application = self
        
        # Get the original application back
        original_application = Application.objects.get(id=old_id)
        
        # Copy fees
        for fee in original_application.fees.all():
            Fee.objects.create(
                application=new_application,
                description=fee.description,
                amount=fee.amount,
                fee_type=fee.fee_type,
                status='WAITING'  # Reset status for the new application
            )
        
        return new_application

class Fee(models.Model):
    """
    Fee model for tracking application fees
    """
    STATUS_CHOICES = [
        ('PAID', 'Paid'),
        ('WAITING', 'Waiting Payment'),
    ]
    
    FEE_TYPE_CHOICES = [
        ('ESTABLISHMENT', 'Establishment Fee'),
        ('VALUATION', 'Valuation Fee'),
        ('LEGAL', 'Legal Fee'),
        ('BROKER', 'Broker Commission'),
        ('OTHER', 'Other Fee'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='fees')
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    fee_type = models.CharField(max_length=20, choices=FEE_TYPE_CHOICES, default='OTHER')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='WAITING')
    invoice = models.FileField(upload_to=invoice_upload_path, null=True, blank=True)
    payment_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.get_fee_type_display()} - {self.amount} for {self.application.id}"

class Payment(models.Model):
    """
    Payment ledger for tracking payments received/made
    """
    PAYMENT_TYPE_CHOICES = [
        ('RECEIVED', 'Payment Received'),
        ('MADE', 'Payment Made'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('BANK_TRANSFER', 'Bank Transfer'),
        ('CREDIT_CARD', 'Credit Card'),
        ('CASH', 'Cash'),
        ('CHECK', 'Check'),
        ('OTHER', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='payments')
    fee = models.ForeignKey(Fee, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPE_CHOICES)
    payment_method = models.CharField(max_length=15, choices=PAYMENT_METHOD_CHOICES, default='BANK_TRANSFER')
    payment_date = models.DateField()
    reference = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.get_payment_type_display()} - {self.amount} for {self.application.id}"

class Note(models.Model):
    """
    Notes attached to applications
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='notes')
    content = models.TextField()
    remind_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Note for {self.application.id}"

class Repayment(models.Model):
    """
    Repayment schedule for applications
    """
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('OVERDUE', 'Overdue'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='repayments')
    due_date = models.DateField()
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    payment_date = models.DateField(null=True, blank=True)
    invoice = models.FileField(upload_to=invoice_upload_path, null=True, blank=True)
    
    def __str__(self):
        return f"Repayment for {self.application.id} due on {self.due_date}"

class Extension(models.Model):
    """
    Loan extension information
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='extensions')
    new_loan_amount = models.DecimalField(max_digits=15, decimal_places=2)
    new_rate = models.DecimalField(max_digits=5, decimal_places=2)
    new_terms = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Extension for {self.application.id}"
