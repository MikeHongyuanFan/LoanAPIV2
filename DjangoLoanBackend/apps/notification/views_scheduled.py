from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta

from .models import Notification
from apps.application.models import Application, Repayment
from apps.authentication.permissions import IsStaff


class RepaymentReminderView(APIView):
    """
    API endpoint for sending repayment reminders.
    """
    permission_classes = [IsAuthenticated, IsStaff]
    
    def post(self, request):
        # Get days before due date to send reminder
        days_before = request.data.get('days_before', 7)
        
        try:
            days_before = int(days_before)
        except ValueError:
            return Response({
                'error': 'days_before must be an integer'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Calculate target date
        today = timezone.now().date()
        target_date = today + timedelta(days=days_before)
        
        # Find repayments due on target date
        repayments = Repayment.objects.filter(
            due_date=target_date,
            status='PENDING'
        ).select_related('application', 'application__borrower')
        
        # Send reminders
        sent_count = 0
        for repayment in repayments:
            # Skip if borrower has no email
            if not repayment.application.borrower or not repayment.application.borrower.email:
                continue
            
            # Create notification
            notification = Notification.objects.create(
                type='REPAYMENT_REMINDER',
                recipient_email=repayment.application.borrower.email,
                subject=f"Repayment Reminder: {repayment.application.reference_number}",
                message=f"Dear {repayment.application.borrower.name},\n\n"
                        f"This is a reminder that your repayment of ${repayment.amount} is due on {repayment.due_date}.\n\n"
                        f"Please ensure funds are available for this payment.\n\n"
                        f"Regards,\nLoan Application System",
                status='PENDING',
                created_by=request.user.profile if hasattr(request.user, 'profile') else None
            )
            
            # In a real implementation, this would be sent via a task queue
            # For now, just mark as sent
            notification.status = 'SENT'
            notification.save()
            sent_count += 1
        
        return Response({
            'message': f'Sent {sent_count} repayment reminders for payments due in {days_before} days',
            'sent_count': sent_count,
            'target_date': target_date
        })


class LateRepaymentReminderView(APIView):
    """
    API endpoint for sending late repayment reminders.
    """
    permission_classes = [IsAuthenticated, IsStaff]
    
    def post(self, request):
        # Get days after due date to send reminder
        days_after = request.data.get('days_after', [3, 7, 10])
        
        if not isinstance(days_after, list):
            days_after = [days_after]
        
        # Calculate target dates
        today = timezone.now().date()
        target_dates = [today - timedelta(days=days) for days in days_after]
        
        # Find late repayments
        repayments = Repayment.objects.filter(
            due_date__in=target_dates,
            status='PENDING'
        ).select_related('application', 'application__borrower')
        
        # Update status to overdue
        for repayment in repayments:
            repayment.status = 'OVERDUE'
            repayment.save()
        
        # Send reminders
        sent_count = 0
        for repayment in repayments:
            # Skip if borrower has no email
            if not repayment.application.borrower or not repayment.application.borrower.email:
                continue
            
            # Calculate days overdue
            days_overdue = (today - repayment.due_date).days
            
            # Create notification
            notification = Notification.objects.create(
                type='LATE_REPAYMENT',
                recipient_email=repayment.application.borrower.email,
                subject=f"OVERDUE Repayment: {repayment.application.reference_number}",
                message=f"Dear {repayment.application.borrower.name},\n\n"
                        f"Your repayment of ${repayment.amount} was due on {repayment.due_date} "
                        f"and is now {days_overdue} days overdue.\n\n"
                        f"Please make this payment as soon as possible to avoid additional fees.\n\n"
                        f"Regards,\nLoan Application System",
                status='PENDING',
                created_by=request.user.profile if hasattr(request.user, 'profile') else None
            )
            
            # In a real implementation, this would be sent via a task queue
            # For now, just mark as sent
            notification.status = 'SENT'
            notification.save()
            sent_count += 1
            
            # If 10 days overdue, also notify BD
            if days_overdue == 10 and repayment.application.assigned_to and repayment.application.assigned_to.user.email:
                bd_notification = Notification.objects.create(
                    type='BD_LATE_REPAYMENT',
                    recipient_email=repayment.application.assigned_to.user.email,
                    subject=f"Action Required: 10-Day Overdue Repayment - {repayment.application.reference_number}",
                    message=f"Dear {repayment.application.assigned_to.user.first_name},\n\n"
                            f"The repayment of ${repayment.amount} for application {repayment.application.reference_number} "
                            f"was due on {repayment.due_date} and is now 10 days overdue.\n\n"
                            f"Please contact the borrower ({repayment.application.borrower.name}) to resolve this issue.\n\n"
                            f"Regards,\nLoan Application System",
                    status='SENT',
                    created_by=request.user.profile if hasattr(request.user, 'profile') else None
                )
        
        return Response({
            'message': f'Processed {len(repayments)} late repayments and sent {sent_count} reminders',
            'processed_count': len(repayments),
            'sent_count': sent_count,
            'days_after': days_after
        })


class LoanExpirationReminderView(APIView):
    """
    API endpoint for sending loan expiration reminders.
    """
    permission_classes = [IsAuthenticated, IsStaff]
    
    def post(self, request):
        # Get days before expiration to send reminder
        days_before = request.data.get('days_before', 30)
        
        try:
            days_before = int(days_before)
        except ValueError:
            return Response({
                'error': 'days_before must be an integer'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Calculate target date
        today = timezone.now().date()
        target_date = today + timedelta(days=days_before)
        
        # Find applications with term ending on target date
        # This is a simplified approach - in a real system, you would calculate the actual end date
        # based on settlement date and term_months
        applications = Application.objects.filter(
            status='APPROVED',
            created_at__date=target_date - timedelta(days=30 * 12)  # Assuming 12-month terms for simplicity
        ).select_related('borrower', 'assigned_to')
        
        # Send reminders
        sent_count = 0
        for application in applications:
            # Skip if borrower has no email
            if not application.borrower or not application.borrower.email:
                continue
            
            # Create notification for borrower
            notification = Notification.objects.create(
                type='LOAN_EXPIRATION',
                recipient_email=application.borrower.email,
                subject=f"Loan Expiration Notice: {application.reference_number}",
                message=f"Dear {application.borrower.name},\n\n"
                        f"Your loan (Reference: {application.reference_number}) is set to expire in {days_before} days.\n\n"
                        f"Please contact us to discuss your options for repayment or extension.\n\n"
                        f"Regards,\nLoan Application System",
                status='PENDING',
                created_by=request.user.profile if hasattr(request.user, 'profile') else None
            )
            
            # In a real implementation, this would be sent via a task queue
            # For now, just mark as sent
            notification.status = 'SENT'
            notification.save()
            sent_count += 1
            
            # Also notify BD if assigned
            if application.assigned_to and application.assigned_to.user.email:
                bd_notification = Notification.objects.create(
                    type='BD_LOAN_EXPIRATION',
                    recipient_email=application.assigned_to.user.email,
                    subject=f"Loan Expiration Alert: {application.reference_number}",
                    message=f"Dear {application.assigned_to.user.first_name},\n\n"
                            f"The loan for application {application.reference_number} is set to expire in {days_before} days.\n\n"
                            f"Please contact the borrower ({application.borrower.name}) to discuss repayment or extension options.\n\n"
                            f"Regards,\nLoan Application System",
                    status='SENT',
                    created_by=request.user.profile if hasattr(request.user, 'profile') else None
                )
        
        return Response({
            'message': f'Sent {sent_count} loan expiration reminders for loans expiring in {days_before} days',
            'sent_count': sent_count,
            'target_date': target_date
        })


class StagnantStageReminderView(APIView):
    """
    API endpoint for sending reminders about applications that have been in the same stage for too long.
    """
    permission_classes = [IsAuthenticated, IsStaff]
    
    def post(self, request):
        # Get days in same stage to trigger reminder
        days_in_stage = request.data.get('days_in_stage', 7)
        
        try:
            days_in_stage = int(days_in_stage)
        except ValueError:
            return Response({
                'error': 'days_in_stage must be an integer'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Calculate cutoff date
        today = timezone.now().date()
        cutoff_date = today - timedelta(days=days_in_stage)
        
        # Find applications that haven't been updated since cutoff date
        # This is a simplified approach - in a real system, you would track stage changes
        applications = Application.objects.filter(
            status__in=['SUBMITTED', 'PROCESSING'],
            updated_at__date__lte=cutoff_date
        ).select_related('assigned_to')
        
        # Send reminders
        sent_count = 0
        for application in applications:
            # Skip if no BD assigned
            if not application.assigned_to or not application.assigned_to.user.email:
                continue
            
            # Create notification
            notification = Notification.objects.create(
                type='STAGNANT_STAGE',
                recipient_email=application.assigned_to.user.email,
                subject=f"Stagnant Application Alert: {application.reference_number}",
                message=f"Dear {application.assigned_to.user.first_name},\n\n"
                        f"Application {application.reference_number} has been in the '{application.stage}' stage "
                        f"for {days_in_stage} days without any updates.\n\n"
                        f"Please review this application and take appropriate action.\n\n"
                        f"Regards,\nLoan Application System",
                status='PENDING',
                created_by=request.user.profile if hasattr(request.user, 'profile') else None
            )
            
            # In a real implementation, this would be sent via a task queue
            # For now, just mark as sent
            notification.status = 'SENT'
            notification.save()
            sent_count += 1
        
        return Response({
            'message': f'Sent {sent_count} stagnant stage reminders for applications unchanged for {days_in_stage} days',
            'sent_count': sent_count,
            'cutoff_date': cutoff_date
        })
