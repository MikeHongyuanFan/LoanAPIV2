from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from .models import Application, Extension
from apps.notification.models import Notification
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=Application)
def application_status_change(sender, instance, created, **kwargs):
    """
    Create notifications when application status changes.
    """
    if not created and hasattr(instance, '_original_status') and instance._original_status != instance.status:
        # Create notification for status change
        Notification.objects.create(
            type='STAGE_CHANGE',
            subject=f'Application status changed to {instance.get_status_display()}',
            message=f'The status of application {instance.reference_number} has been changed from {instance._original_status} to {instance.status}',
            related_id=instance.id,
            related_entity='APPLICATION',
            trigger_date=timezone.now(),
            status='PENDING'
        )

@receiver(post_save, sender=Application)
def application_stage_change(sender, instance, created, **kwargs):
    """
    Create notifications and send emails when application stage changes.
    """
    if not created and hasattr(instance, '_original_stage') and instance._original_stage != instance.stage:
        # Create notification for stage change
        Notification.objects.create(
            type='STAGE_CHANGE',
            subject=f'Application stage changed to {instance.get_stage_display()}',
            message=f'The stage of application {instance.reference_number} has been changed from {instance._original_stage} to {instance.stage}',
            related_id=instance.id,
            related_entity='APPLICATION',
            trigger_date=timezone.now(),
            status='PENDING'
        )
        
        # Send email to broker if broker exists
        if instance.broker and instance.broker.email:
            send_mail(
                subject=f'Application {instance.reference_number} Stage Update',
                message=f'The application {instance.reference_number} has moved to the {instance.get_stage_display()} stage.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.broker.email],
                fail_silently=True,
            )
        
        # Send email to borrower if borrower exists
        if instance.borrower and instance.borrower.email:
            send_mail(
                subject=f'Your Loan Application {instance.reference_number} Update',
                message=f'Your loan application {instance.reference_number} has moved to the {instance.get_stage_display()} stage.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.borrower.email],
                fail_silently=True,
            )

@receiver(pre_save, sender=Application)
def application_stagnation_check(sender, instance, **kwargs):
    """
    Create notifications when application stays in the same stage too long.
    """
    if not instance.pk:
        return
    
    try:
        old_instance = Application.objects.get(pk=instance.pk)
        
        # Check for stage stagnation
        if old_instance.stage == instance.stage:
            # Get stage-specific threshold (configurable)
            stage_thresholds = {
                'ENQUIRY': 3,  # 3 days
                'INDICATIVE_OFFER': 5,  # 5 days
                'VALUATION': 7,  # 7 days
                'DUAL': 5,  # 5 days
                'FORMAL_APPROVAL': 3,  # 3 days
                'LOAN_DOCS_ISSUED': 10,  # 10 days
                'LOAN_DOCS_RETURN': 5,  # 5 days
                'SETTLEMENT': 3,  # 3 days
                'REJECT': 30,  # 30 days (not really applicable)
                'WITHDRAWAL': 30,  # 30 days (not really applicable)
            }
            
            stagnation_days = stage_thresholds.get(instance.stage, 14)  # Default to 14 days if stage not found
            
            # If stage hasn't changed and it's been more than stagnation_days
            if instance.stage_changed_at < timezone.now() - timedelta(days=stagnation_days):
                # Create notification for stagnation
                Notification.objects.create(
                    type='STAGE_STAGNATION',
                    subject=f'Application stagnant in {instance.get_stage_display()} stage',
                    message=f'The application {instance.reference_number} has been in {instance.stage} stage for more than {stagnation_days} days',
                    related_id=instance.id,
                    related_entity='APPLICATION',
                    trigger_date=timezone.now(),
                    status='PENDING'
                )
                
                # If there's a BD assigned, send notification to them
                if hasattr(instance, 'bd') and instance.bd:
                    Notification.objects.create(
                        type='BD_ALERT',
                        subject=f'Action required: Application stagnant in {instance.get_stage_display()} stage',
                        message=f'The application {instance.reference_number} has been in {instance.stage} stage for more than {stagnation_days} days. Please review and take action.',
                        related_id=instance.id,
                        related_entity='APPLICATION',
                        trigger_date=timezone.now(),
                        status='PENDING',
                        recipient_id=instance.bd.id
                    )
    except Application.DoesNotExist:
        pass

@receiver(post_save, sender=Extension)
def extension_notification(sender, instance, created, **kwargs):
    """
    Create notifications for extension requests and status changes.
    """
    if created:
        # Create notification for new extension request
        Notification.objects.create(
            type='EXTENSION_REQUEST',
            subject=f'New extension request for {instance.application.reference_number}',
            message=f'A new extension request has been created for application {instance.application.reference_number}',
            related_id=instance.id,
            related_entity='EXTENSION',
            trigger_date=timezone.now(),
            status='PENDING'
        )
    elif hasattr(instance, '_original_status') and instance._original_status != instance.status:
        # Create notification for extension status change
        Notification.objects.create(
            type='EXTENSION_STATUS',
            subject=f'Extension request {instance.status.lower()}',
            message=f'The extension request for application {instance.application.reference_number} has been {instance.status.lower()}',
            related_id=instance.id,
            related_entity='EXTENSION',
            trigger_date=timezone.now(),
            status='PENDING'
        )
