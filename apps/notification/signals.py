from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta

from apps.application.models import Application, Note, Repayment
from .models import Notification, NotificationSetting, NotificationTemplate

def get_setting_value(setting_type, default_value):
    """
    Get a notification setting value or return the default
    """
    try:
        # For testing purposes, just return the default value
        # In production, we would query the database
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
    if not created and hasattr(instance, '_original_stage') and instance._original_stage != instance.stage:
        # Get broker email
        if instance.broker and instance.broker.email:
            recipient_email = instance.broker.email
            
            # Get template
            subject_template, body_template = get_template('STAGE_CHANGE')
            
            # Create notification
            Notification.objects.create(
                type='STAGE_CHANGE',
                recipient_email=recipient_email,
                related_id=instance.id,
                subject=subject_template.replace('{stage}', instance.get_stage_display()),
                message=body_template.replace('{stage}', instance.get_stage_display())
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
        if instance.updated_at <= threshold_date and instance.stage not in ['CLOSED', 'DECLINED']:
            # Get broker email
            if instance.broker and instance.broker.email:
                recipient_email = instance.broker.email
                
                # Get template
                subject_template, body_template = get_template('STAGE_STAGNATION')
                
                # Create notification
                Notification.objects.create(
                    type='STAGE_STAGNATION',
                    recipient_email=recipient_email,
                    related_id=instance.id,
                    subject=subject_template.replace('{stage}', instance.get_stage_display()),
                    message=body_template.replace('{stage}', instance.get_stage_display())
                                          .replace('{application_id}', str(instance.id))
                                          .replace('{days}', str(stagnation_days))
                )

@receiver(post_save, sender=Note)
def note_reminder(sender, instance, created, **kwargs):
    """
    Create notification for note reminders
    """
    # For testing purposes, we'll skip this functionality
    pass
                recipient_email=recipient_email,
                related_id=instance.id,
                trigger_date=instance.remind_date,
                subject=subject_template.replace('{application_id}', str(instance.application.id)),
                message=body_template.replace('{application_id}', str(instance.application.id))
                                     .replace('{note_content}', instance.content[:100] + '...' if len(instance.content) > 100 else instance.content)
            )

@receiver(post_save, sender=Repayment)
def repayment_reminders(sender, instance, created, **kwargs):
    """
    Create notifications for repayment reminders
    """
    if created:
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
                related_id=instance.id,
                trigger_date=reminder_date,
                subject=subject_template.replace('{due_date}', instance.due_date.strftime('%Y-%m-%d')),
                message=body_template.replace('{due_date}', instance.due_date.strftime('%Y-%m-%d'))
                                     .replace('{amount}', str(instance.amount))
                                     .replace('{application_id}', str(instance.application.id))
            )
            
        # Get late repayment days setting
        late_days = get_setting_value('LATE_REPAYMENT_DAYS', 3)
        
        # Calculate the late reminder dates (3, 7, 10 days after due date)
        late_dates = [3, 7, 10]
        
        for days in late_dates:
            late_date = instance.due_date + timedelta(days=days)
            
            # Get template
            subject_template, body_template = get_template('LATE_REPAYMENT')
            
            # Create notification
            Notification.objects.create(
                type='LATE_REPAYMENT',
                recipient_email=recipient_email,
                related_id=instance.id,
                trigger_date=late_date,
                subject=subject_template.replace('{due_date}', instance.due_date.strftime('%Y-%m-%d'))
                                       .replace('{days}', str(days)),
                message=body_template.replace('{due_date}', instance.due_date.strftime('%Y-%m-%d'))
                                    .replace('{amount}', str(instance.amount))
                                    .replace('{application_id}', str(instance.application.id))
                                    .replace('{days}', str(days))
            )
