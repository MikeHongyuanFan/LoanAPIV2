from django.db import models
from django.utils import timezone


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
    
    def __str__(self):
        return f"{self.name} ({self.company})"


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
    
    def __str__(self):
        return f"Commission for {self.broker.name} - {self.application.reference_number}"


class CommissionPayment(models.Model):
    payment_date = models.DateField()
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    reference_number = models.CharField(max_length=100)
    notes = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey('authentication.UserProfile', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Payment {self.reference_number} on {self.payment_date}"


class CommissionPaymentItem(models.Model):
    payment = models.ForeignKey(CommissionPayment, on_delete=models.CASCADE, related_name='items')
    commission = models.ForeignKey(BrokerCommission, on_delete=models.CASCADE, related_name='payment_items')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    
    def __str__(self):
        return f"Payment item for {self.commission}"
