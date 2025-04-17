from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from .models import Application, Extension
from apps.notification.models import Notification

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

@receiver(pre_save, sender=Application)
def application_stagnation_check(sender, instance, **kwargs):
    """
    Create notifications when application stays in the same stage too long.
    """
    if not instance.pk:
        return
    
    try:
        old_instance = Application.objects.get(pk=instance.pk)
        stagnation_days = 14  # Default threshold
        
        # If status hasn't changed and it's been more than stagnation_days
        if (old_instance.status == instance.status and 
            old_instance.updated_at < timezone.now() - timedelta(days=stagnation_days)):
            
            # Create notification for stagnation
            Notification.objects.create(
                type='STAGE_STAGNATION',
                subject=f'Application stagnant in {instance.get_status_display()} stage',
                message=f'The application {instance.reference_number} has been in {instance.status} stage for more than {stagnation_days} days',
                related_id=instance.id,
                related_entity='APPLICATION',
                trigger_date=timezone.now(),
                status='PENDING'
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
