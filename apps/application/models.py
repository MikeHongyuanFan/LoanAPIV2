import uuid
from django.db import models
from django.utils import timezone

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
    
    def __str__(self):
        return f"Application {self.id} - {self.borrower.name}"

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
