from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Sum, Avg, F, Q
from django.utils import timezone
from datetime import timedelta

from apps.application.models import Application, Repayment
from apps.broker.models import Broker, BrokerCommission
from apps.authentication.permissions import IsStaff, IsManager


class DashboardSummaryView(APIView):
    """
    API endpoint for retrieving dashboard summary data.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Get date range parameters
        period = request.query_params.get('period', 'month')  # day, week, month, quarter, year
        
        # Calculate date range
        today = timezone.now().date()
        if period == 'day':
            start_date = today
        elif period == 'week':
            start_date = today - timedelta(days=7)
        elif period == 'month':
            start_date = today - timedelta(days=30)
        elif period == 'quarter':
            start_date = today - timedelta(days=90)
        elif period == 'year':
            start_date = today - timedelta(days=365)
        else:
            start_date = today - timedelta(days=30)  # Default to month
        
        # Get applications in the date range
        applications = Application.objects.filter(created_at__gte=start_date)
        
        # Calculate application statistics
        total_applications = applications.count()
        total_loan_amount = applications.aggregate(total=Sum('loan_amount'))['total'] or 0
        
        # Calculate status breakdown
        status_counts = applications.values('status').annotate(count=Count('id')).order_by('status')
        status_breakdown = {item['status']: item['count'] for item in status_counts}
        
        # Calculate stage breakdown
        stage_counts = applications.values('stage').annotate(count=Count('id')).order_by('stage')
        stage_breakdown = {item['stage']: item['count'] for item in stage_counts}
        
        # Get upcoming repayments (due in the next 30 days)
        upcoming_repayments = Repayment.objects.filter(
            due_date__gte=today,
            due_date__lte=today + timedelta(days=30),
            status='PENDING'
        ).order_by('due_date')
        
        upcoming_repayment_data = []
        for repayment in upcoming_repayments[:5]:  # Limit to 5 for dashboard
            upcoming_repayment_data.append({
                'id': repayment.id,
                'application_id': repayment.application.id,
                'reference_number': repayment.application.reference_number,
                'borrower_name': repayment.application.borrower.name if repayment.application.borrower else None,
                'amount': repayment.amount,
                'due_date': repayment.due_date,
                'days_until_due': (repayment.due_date - today).days
            })
        
        # Get recent applications
        recent_applications = Application.objects.all().order_by('-created_at')[:5]
        recent_application_data = []
        
        for app in recent_applications:
            recent_application_data.append({
                'id': app.id,
                'reference_number': app.reference_number,
                'status': app.status,
                'stage': app.stage,
                'loan_amount': app.loan_amount,
                'borrower_name': app.borrower.name if app.borrower else None,
                'broker_name': app.broker.name if app.broker else None,
                'created_at': app.created_at
            })
        
        # Get top brokers by application count
        top_brokers = Broker.objects.annotate(
            application_count=Count('applications'),
            total_loan_amount=Sum('applications__loan_amount')
        ).order_by('-application_count')[:5]
        
        top_broker_data = []
        for broker in top_brokers:
            top_broker_data.append({
                'id': broker.id,
                'name': broker.name,
                'company': broker.company,
                'application_count': broker.application_count,
                'total_loan_amount': broker.total_loan_amount or 0
            })
        
        return Response({
            'period': period,
            'start_date': start_date,
            'end_date': today,
            'application_summary': {
                'total_applications': total_applications,
                'total_loan_amount': total_loan_amount,
                'status_breakdown': status_breakdown,
                'stage_breakdown': stage_breakdown
            },
            'upcoming_repayments': upcoming_repayment_data,
            'recent_applications': recent_application_data,
            'top_brokers': top_broker_data
        })


class UserDashboardView(APIView):
    """
    API endpoint for retrieving user-specific dashboard data.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Get the current user
        user = request.user
        
        # Get applications assigned to the user
        assigned_applications = Application.objects.filter(assigned_to=user.profile)
        
        # Calculate application statistics
        total_assigned = assigned_applications.count()
        
        # Calculate status breakdown
        status_counts = assigned_applications.values('status').annotate(count=Count('id')).order_by('status')
        status_breakdown = {item['status']: item['count'] for item in status_counts}
        
        # Get recent applications assigned to the user
        recent_assigned = assigned_applications.order_by('-created_at')[:5]
        recent_assigned_data = []
        
        for app in recent_assigned:
            recent_assigned_data.append({
                'id': app.id,
                'reference_number': app.reference_number,
                'status': app.status,
                'stage': app.stage,
                'loan_amount': app.loan_amount,
                'borrower_name': app.borrower.name if app.borrower else None,
                'created_at': app.created_at
            })
        
        # Get upcoming tasks (notes with remind dates)
        today = timezone.now().date()
        upcoming_tasks = []
        
        # This would require a Note model with remind_date field
        # For now, we'll return an empty list
        
        return Response({
            'user_id': user.id,
            'username': user.username,
            'assigned_applications': {
                'total': total_assigned,
                'status_breakdown': status_breakdown,
                'recent': recent_assigned_data
            },
            'upcoming_tasks': upcoming_tasks
        })


class ManagerDashboardView(APIView):
    """
    API endpoint for retrieving manager-specific dashboard data.
    """
    permission_classes = [IsAuthenticated, IsManager]
    
    def get(self, request):
        # Get date range parameters
        period = request.query_params.get('period', 'month')  # day, week, month, quarter, year
        
        # Calculate date range
        today = timezone.now().date()
        if period == 'day':
            start_date = today
        elif period == 'week':
            start_date = today - timedelta(days=7)
        elif period == 'month':
            start_date = today - timedelta(days=30)
        elif period == 'quarter':
            start_date = today - timedelta(days=90)
        elif period == 'year':
            start_date = today - timedelta(days=365)
        else:
            start_date = today - timedelta(days=30)  # Default to month
        
        # Get applications in the date range
        applications = Application.objects.filter(created_at__gte=start_date)
        
        # Calculate application statistics
        total_applications = applications.count()
        total_loan_amount = applications.aggregate(total=Sum('loan_amount'))['total'] or 0
        approved_applications = applications.filter(status='APPROVED').count()
        rejected_applications = applications.filter(status='REJECTED').count()
        
        approval_rate = (approved_applications / total_applications * 100) if total_applications > 0 else 0
        
        # Calculate average processing time (in days)
        completed = applications.filter(
            status__in=['APPROVED', 'REJECTED', 'CANCELLED']
        )
        
        avg_processing_time = completed.annotate(
            processing_time=F('updated_at') - F('created_at')
        ).aggregate(
            avg_days=Avg('processing_time')
        )['avg_days']
        
        if avg_processing_time:
            avg_processing_days = avg_processing_time.total_seconds() / (60 * 60 * 24)
        else:
            avg_processing_days = 0
        
        # Calculate stagnant applications (no activity for 7+ days)
        seven_days_ago = timezone.now() - timedelta(days=7)
        stagnant = Application.objects.filter(
            status='PROCESSING',
            updated_at__lt=seven_days_ago
        ).count()
        
        # Calculate commission data
        commissions = BrokerCommission.objects.filter(created_at__gte=start_date)
        total_commission = commissions.aggregate(total=Sum('amount'))['total'] or 0
        paid_commission = commissions.filter(status='PAID').aggregate(total=Sum('amount'))['total'] or 0
        pending_commission = commissions.filter(status='PENDING').aggregate(total=Sum('amount'))['total'] or 0
        
        return Response({
            'period': period,
            'start_date': start_date,
            'end_date': today,
            'application_metrics': {
                'total_applications': total_applications,
                'total_loan_amount': total_loan_amount,
                'approved_applications': approved_applications,
                'rejected_applications': rejected_applications,
                'approval_rate': approval_rate,
                'avg_processing_days': avg_processing_days,
                'stagnant_applications': stagnant
            },
            'commission_metrics': {
                'total_commission': total_commission,
                'paid_commission': paid_commission,
                'pending_commission': pending_commission
            }
        })
