from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from apps.application.models import Application
from .models import BrokerCommission


@receiver(post_save, sender=Application)
def create_broker_commission(sender, instance, created, **kwargs):
    """
    Signal handler to automatically create a broker commission when an application is approved.
    """
    # Only create commission when application status is APPROVED
    if instance.status == 'APPROVED':
        # Check if broker exists and no commission has been created yet
        if instance.broker and not BrokerCommission.objects.filter(application=instance).exists():
            # Calculate commission based on loan amount and product commission rate
            loan_amount = instance.loan_amount
            commission_rate = instance.product.broker_commission_rate if instance.product else 0.01  # Default 1%
            commission_amount = loan_amount * commission_rate
            
            # Create the commission record
            BrokerCommission.objects.create(
                broker=instance.broker,
                application=instance,
                amount=commission_amount,
                percentage=commission_rate * 100,  # Convert to percentage
                status='PENDING'
            )
