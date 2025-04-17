from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta

from apps.application.models import Application, Note, Repayment, Extension, Fee
from .models import Notification, NotificationSetting, NotificationTemplate

def get_setting_value(setting_type, default_value):
    """
    Get a notification setting value or return the default
    """
    try:
        setting = NotificationSetting.objects.get(setting_type=setting_type)
        return setting.value
    except NotificationSetting.DoesNotExist:
        return default_value
    except Exception:
        return default_value

def get_template(notification_type):
    """
    Get a notification template or return default values
    """
    try:
        template = NotificationTemplate.objects.get(type=notification_type)
        return template.subject_template, template.body_template
    except NotificationTemplate.DoesNotExist:
        return f"Default {notification_type} Subject", f"Default {notification_type} Body"

@receiver(post_save, sender=Application)
def application_stage_changed(sender, instance, created, **kwargs):
    """
    Create notification when application stage changes
    """
    if not created and hasattr(instance, '_original_status') and instance._original_status != instance.status:
        # Get broker email
        if instance.broker and instance.broker.email:
            recipient_email = instance.broker.email
            
            # Get template
            subject_template, body_template = get_template('STAGE_CHANGE')
            
            # Create notification
            Notification.objects.create(
                type='STAGE_CHANGE',
                recipient_email=recipient_email,
                related_entity='Application',
                related_id=instance.id,
                subject=subject_template.replace('{stage}', instance.get_status_display()),
                message=body_template.replace('{stage}', instance.get_status_display())
                                      .replace('{application_id}', str(instance.id))
            )
            
            # Also notify borrower if email is available
            if instance.borrower and hasattr(instance.borrower, 'email') and instance.borrower.email:
                Notification.objects.create(
                    type='STAGE_CHANGE',
                    recipient_email=instance.borrower.email,
                    related_entity='Application',
                    related_id=instance.id,
                    subject=subject_template.replace('{stage}', instance.get_status_display()),
                    message=body_template.replace('{stage}', instance.get_status_display())
                                          .replace('{application_id}', str(instance.id))
                )

@receiver(post_save, sender=Application)
def check_stage_stagnation(sender, instance, created, **kwargs):
    """
    Check if an application has been in the same stage for too long
    """
    if not created:
        # Get stagnation days setting
        stagnation_days = get_setting_value('STAGE_STAGNATION_DAYS', 14)
        
        # Calculate the date threshold
        threshold_date = timezone.now() - timedelta(days=stagnation_days)
        
        # Check if the application has been updated before the threshold and is not in a final stage
        if instance.updated_at <= threshold_date and instance.status not in ['CLOSED', 'DECLINED']:
            # Get BD/admin email - in a real system, we would get this from user profiles with BD role
            admin_email = "admin@example.com"  # Placeholder
            
            # Get template
            subject_template, body_template = get_template('STAGE_STAGNATION')
            
            # Create notification
            Notification.objects.create(
                type='STAGE_STAGNATION',
                recipient_email=admin_email,
                related_entity='Application',
                related_id=instance.id,
                subject=subject_template.replace('{stage}', instance.get_status_display()),
                message=body_template.replace('{stage}', instance.get_status_display())
                                      .replace('{application_id}', str(instance.id))
                                      .replace('{days}', str(stagnation_days))
            )

@receiver(post_save, sender=Note)
def note_reminder(sender, instance, created, **kwargs):
    """
    Create notification for note reminders
    """
    if created or (hasattr(instance, '_original_reminder_date') and instance._original_reminder_date != instance.reminder_date):
        if instance.has_reminder and instance.reminder_date and not instance.reminder_sent:
            # Get the user who created the note
            if instance.created_by and hasattr(instance.created_by, 'email') and instance.created_by.email:
                recipient_email = instance.created_by.email
                
                # Get template
                subject_template, body_template = get_template('NOTE_REMINDER')
                
                # Create notification
                Notification.objects.create(
                    type='NOTE_REMINDER',
                    recipient_email=recipient_email,
                    related_entity='Note',
                    related_id=instance.id,
                    trigger_date=instance.reminder_date,
                    subject=subject_template.replace('{application_id}', str(instance.application.id)),
                    message=body_template.replace('{application_id}', str(instance.application.id))
                                         .replace('{note_content}', instance.content[:100] + '...' if len(instance.content) > 100 else instance.content)
                )

@receiver(post_save, sender=Repayment)
def repayment_reminders(sender, instance, created, **kwargs):
    """
    Create notifications for repayment reminders
    """
    if created or (hasattr(instance, '_original_due_date') and instance._original_due_date != instance.due_date):
        # Get reminder days setting
        reminder_days = get_setting_value('REPAYMENT_REMINDER_DAYS', 7)
        
        # Calculate the reminder date
        reminder_date = instance.due_date - timedelta(days=reminder_days)
        
        # Get borrower email
        if instance.application.borrower and hasattr(instance.application.borrower, 'email') and instance.application.borrower.email:
            recipient_email = instance.application.borrower.email
            
            # Get template
            subject_template, body_template = get_template('REPAYMENT_REMINDER')
            
            # Create notification
            Notification.objects.create(
                type='REPAYMENT_REMINDER',
                recipient_email=recipient_email,
                related_entity='Repayment',
                related_id=instance.id,
                trigger_date=reminder_date,
                subject=subject_template.replace('{due_date}', instance.due_date.strftime('%Y-%m-%d')),
                message=body_template.replace('{due_date}', instance.due_date.strftime('%Y-%m-%d'))
                                     .replace('{amount}', str(instance.amount))
                                     .replace('{application_id}', str(instance.application.id))
            )
            
        # Get late repayment days setting
        late_days = [3, 7, 10]  # Days after due date for reminders
        
        for days in late_days:
            late_date = instance.due_date + timedelta(days=days)
            
            # Get template
            subject_template, body_template = get_template('LATE_REPAYMENT')
            
            # Create notification for borrower
            if instance.application.borrower and hasattr(instance.application.borrower, 'email') and instance.application.borrower.email:
                Notification.objects.create(
                    type='LATE_REPAYMENT',
                    recipient_email=instance.application.borrower.email,
                    related_entity='Repayment',
                    related_id=instance.id,
                    trigger_date=late_date,
                    subject=subject_template.replace('{due_date}', instance.due_date.strftime('%Y-%m-%d'))
                                           .replace('{days}', str(days)),
                    message=body_template.replace('{due_date}', instance.due_date.strftime('%Y-%m-%d'))
                                        .replace('{amount}', str(instance.amount))
                                        .replace('{application_id}', str(instance.application.id))
                                        .replace('{days}', str(days))
                )
            
            # For 10 days late, also notify BD/admin
            if days == 10:
                admin_email = "admin@example.com"  # Placeholder
                
                Notification.objects.create(
                    type='LATE_REPAYMENT_ADMIN',
                    recipient_email=admin_email,
                    related_entity='Repayment',
                    related_id=instance.id,
                    trigger_date=late_date,
                    subject=f"ACTION REQUIRED: Repayment for Application {instance.application.reference_number} is 10 days overdue",
                    message=f"The repayment of ${instance.amount} for Application {instance.application.reference_number} "
                            f"was due on {instance.due_date.strftime('%Y-%m-%d')} and is now 10 days overdue. "
                            f"Please contact the borrower immediately."
                )

@receiver(post_save, sender=Extension)
def extension_notifications(sender, instance, created, **kwargs):
    """
    Create notifications for loan extensions
    """
    if created:
        # Notify admin about new extension request
        admin_email = "admin@example.com"  # Placeholder
        
        Notification.objects.create(
            type='EXTENSION_REQUEST',
            recipient_email=admin_email,
            related_entity='Extension',
            related_id=instance.id,
            subject=f"New Loan Extension Request for {instance.application.reference_number}",
            message=f"A new loan extension request has been submitted for Application {instance.application.reference_number}. "
                    f"Original expiry date: {instance.original_expiry_date.strftime('%Y-%m-%d')}. "
                    f"Requested new expiry date: {instance.new_expiry_date.strftime('%Y-%m-%d')}. "
                    f"Reason: {instance.reason}"
        )
    
    elif hasattr(instance, '_original_status') and instance._original_status != instance.status:
        # Notify borrower and broker about extension status change
        recipients = []
        
        if instance.application.borrower and hasattr(instance.application.borrower, 'email') and instance.application.borrower.email:
            recipients.append(instance.application.borrower.email)
            
        if instance.application.broker and instance.application.broker.email:
            recipients.append(instance.application.broker.email)
            
        for recipient in recipients:
            Notification.objects.create(
                type='EXTENSION_STATUS',
                recipient_email=recipient,
                related_entity='Extension',
                related_id=instance.id,
                subject=f"Loan Extension {instance.status} for {instance.application.reference_number}",
                message=f"The loan extension request for Application {instance.application.reference_number} has been {instance.status}. "
                        f"New expiry date: {instance.new_expiry_date.strftime('%Y-%m-%d') if instance.status == 'APPROVED' else 'N/A'}"
            )

@receiver(post_save, sender=Fee)
def fee_status_notification(sender, instance, created, **kwargs):
    """
    Create notifications for fee status changes
    """
    if not created and hasattr(instance, '_original_status') and instance._original_status != instance.status:
        # Notify borrower about fee status change
        if instance.application.borrower and hasattr(instance.application.borrower, 'email') and instance.application.borrower.email:
            recipient_email = instance.application.borrower.email
            
            Notification.objects.create(
                type='FEE_STATUS',
                recipient_email=recipient_email,
                related_entity='Fee',
                related_id=instance.id,
                subject=f"Fee Status Update for {instance.application.reference_number}",
                message=f"The status of {instance.get_fee_type_display()} for Application {instance.application.reference_number} "
                        f"has been updated to {instance.get_status_display()}. "
                        f"Amount: ${instance.amount}"
            )

@receiver(post_save, sender=Application)
def loan_expiration_notification(sender, instance, created, **kwargs):
    """
    Create notifications for loan expiration
    """
    if instance.expiry_date:
        # Get expiration reminder days setting
        expiration_days = get_setting_value('LOAN_EXPIRATION_DAYS', 30)
        
        # Calculate the reminder date
        reminder_date = instance.expiry_date - timedelta(days=expiration_days)
        
        recipients = []
        
        # Add borrower if email available
        if instance.borrower and hasattr(instance.borrower, 'email') and instance.borrower.email:
            recipients.append(instance.borrower.email)
            
        # Add broker if email available
        if instance.broker and instance.broker.email:
            recipients.append(instance.broker.email)
            
        # Add BD/admin
        recipients.append("admin@example.com")  # Placeholder
        
        # Get template
        subject_template, body_template = get_template('LOAN_EXPIRATION')
        
        for recipient in recipients:
            Notification.objects.create(
                type='LOAN_EXPIRATION',
                recipient_email=recipient,
                related_entity='Application',
                related_id=instance.id,
                trigger_date=reminder_date,
                subject=subject_template.replace('{expiry_date}', instance.expiry_date.strftime('%Y-%m-%d')),
                message=body_template.replace('{expiry_date}', instance.expiry_date.strftime('%Y-%m-%d'))
                                     .replace('{application_id}', str(instance.id))
                                     .replace('{days}', str(expiration_days))
            )
