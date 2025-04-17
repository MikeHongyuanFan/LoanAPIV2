from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.application.models import Application
from apps.notification.models import Notification
from django.conf import settings
from django.core.mail import send_mail

class Command(BaseCommand):
    help = 'Check for applications that have been in the same stage for too long'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Run without creating notifications or sending emails',
        )

    def handle(self, *args, **options):
        dry_run = options.get('dry_run', False)
        
        # Stage-specific thresholds (configurable)
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
        
        default_threshold = 14  # Default to 14 days if stage not found
        
        # Get all active applications
        applications = Application.objects.exclude(stage__in=['REJECT', 'WITHDRAWAL', 'SETTLEMENT'])
        
        stagnant_count = 0
        for app in applications:
            # Get threshold for this stage
            threshold = stage_thresholds.get(app.stage, default_threshold)
            
            # Check if application has been in the same stage for too long
            if app.stage_changed_at < timezone.now() - timedelta(days=threshold):
                stagnant_count += 1
                self.stdout.write(f"Application {app.reference_number} has been in {app.stage} stage for more than {threshold} days")
                
                if not dry_run:
                    # Create notification for stagnation
                    Notification.objects.create(
                        type='STAGE_STAGNATION',
                        subject=f'Application stagnant in {app.get_stage_display()} stage',
                        message=f'The application {app.reference_number} has been in {app.stage} stage for more than {threshold} days',
                        related_id=app.id,
                        related_entity='APPLICATION',
                        trigger_date=timezone.now(),
                        status='PENDING'
                    )
                    
                    # If there's a BD assigned, send notification to them
                    if hasattr(app, 'bd') and app.bd:
                        Notification.objects.create(
                            type='BD_ALERT',
                            subject=f'Action required: Application stagnant in {app.get_stage_display()} stage',
                            message=f'The application {app.reference_number} has been in {app.stage} stage for more than {threshold} days. Please review and take action.',
                            related_id=app.id,
                            related_entity='APPLICATION',
                            trigger_date=timezone.now(),
                            status='PENDING',
                            recipient_id=app.bd.id
                        )
                        
                        # Send email to BD
                        if app.bd.email:
                            send_mail(
                                subject=f'Action required: Application {app.reference_number} stagnant',
                                message=f'The application {app.reference_number} has been in {app.get_stage_display()} stage for more than {threshold} days. Please review and take action.',
                                from_email=settings.DEFAULT_FROM_EMAIL,
                                recipient_list=[app.bd.email],
                                fail_silently=True,
                            )
        
        if stagnant_count == 0:
            self.stdout.write(self.style.SUCCESS('No stagnant applications found'))
        else:
            self.stdout.write(self.style.WARNING(f'Found {stagnant_count} stagnant applications'))
            if dry_run:
                self.stdout.write(self.style.WARNING('Dry run - no notifications or emails sent'))
