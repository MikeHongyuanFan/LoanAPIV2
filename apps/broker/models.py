from django.db import models
from django.utils import timezone


class Broker(models.Model):
    """
    Model representing a broker who refers loan applications.
    """
    name = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    license_number = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.company})"


class BrokerCommission(models.Model):
    """
    Model representing commission payments to brokers for referred applications.
    """
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    broker = models.ForeignKey('Broker', on_delete=models.CASCADE, related_name='commissions')
    application = models.ForeignKey('application.Application', on_delete=models.CASCADE, related_name='broker_commissions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    payment_date = models.DateField(null=True, blank=True)
    payment_reference = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Commission for {self.broker} - {self.application} - {self.amount}"

    class Meta:
        ordering = ['-created_at']


class CommissionPayment(models.Model):
    """
    Model representing a batch payment of multiple commissions to a broker.
    """
    broker = models.ForeignKey('Broker', on_delete=models.CASCADE, related_name='commission_payments')
    payment_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    reference_number = models.CharField(max_length=100)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment to {self.broker} - {self.payment_date} - {self.total_amount}"

    class Meta:
        ordering = ['-payment_date']


class CommissionPaymentItem(models.Model):
    """
    Model representing individual commission items included in a batch payment.
    """
    payment = models.ForeignKey('CommissionPayment', on_delete=models.CASCADE, related_name='items')
    commission = models.ForeignKey('BrokerCommission', on_delete=models.CASCADE, related_name='payment_items')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Payment item for {self.commission}"
