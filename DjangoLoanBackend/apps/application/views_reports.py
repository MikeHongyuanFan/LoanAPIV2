from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Sum, Avg, F, Q
from django.utils import timezone
from datetime import timedelta
from django_filters.rest_framework import DjangoFilterBackend

from .models import Application, Repayment
from apps.authentication.permissions import IsManager, IsStaff


class ApplicationStatisticsView(APIView):
    """
    API endpoint for retrieving application statistics.
    """
    permission_classes = [IsAuthenticated, IsStaff]
    
    def get(self, request):
        # Get query parameters for date filtering
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        # Base queryset
        queryset = Application.objects.all()
        
        # Apply date filtering if provided
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)
        
        # Calculate statistics
        total_applications = queryset.count()
        total_loan_amount = queryset.aggregate(total=Sum('loan_amount'))['total'] or 0
        average_loan_amount = queryset.aggregate(avg=Avg('loan_amount'))['avg'] or 0
        
        # Status breakdown
        status_counts = queryset.values('status').annotate(count=Count('id')).order_by('status')
        status_breakdown = {item['status']: item['count'] for item in status_counts}
        
        # Stage breakdown
        stage_counts = queryset.values('stage').annotate(count=Count('id')).order_by('stage')
        stage_breakdown = {item['stage']: item['count'] for item in stage_counts}
        
        # Broker breakdown
        broker_counts = queryset.values('broker__name').annotate(
            count=Count('id'),
            total_amount=Sum('loan_amount')
        ).order_by('-count')
        
        # Monthly trend
        monthly_trend = queryset.extra(
            select={'month': "DATE_TRUNC('month', created_at)"}
        ).values('month').annotate(
            count=Count('id'),
            total_amount=Sum('loan_amount')
        ).order_by('month')
        
        return Response({
            'total_applications': total_applications,
            'total_loan_amount': total_loan_amount,
            'average_loan_amount': average_loan_amount,
            'status_breakdown': status_breakdown,
            'stage_breakdown': stage_breakdown,
            'broker_breakdown': list(broker_counts),
            'monthly_trend': list(monthly_trend)
        })


class ApplicationPerformanceView(APIView):
    """
    API endpoint for retrieving application processing performance metrics.
    """
    permission_classes = [IsAuthenticated, IsManager]
    
    def get(self, request):
        # Get query parameters for date filtering
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        # Base queryset for completed applications
        completed = Application.objects.filter(
            status__in=['APPROVED', 'REJECTED', 'CANCELLED']
        )
        
        # Apply date filtering if provided
        if start_date:
            completed = completed.filter(updated_at__gte=start_date)
        if end_date:
            completed = completed.filter(updated_at__lte=end_date)
        
        # Calculate average processing time (in days)
        avg_processing_time = completed.annotate(
            processing_time=F('updated_at') - F('created_at')
        ).aggregate(
            avg_days=Avg('processing_time')
        )['avg_days']
        
        if avg_processing_time:
            avg_processing_days = avg_processing_time.total_seconds() / (60 * 60 * 24)
        else:
            avg_processing_days = 0
        
        # Calculate stage transition times
        stage_times = {}
        stages = ['INQUIRY', 'APPLICATION', 'PROCESSING', 'UNDERWRITING', 'APPROVAL', 'SETTLEMENT']
        
        for i in range(len(stages) - 1):
            current_stage = stages[i]
            next_stage = stages[i + 1]
            
            # This would require stage history tracking which is not implemented yet
            # For now, we'll return placeholder data
            stage_times[f"{current_stage}_to_{next_stage}"] = {
                'avg_days': 2.5,  # Placeholder
                'min_days': 1.0,  # Placeholder
                'max_days': 5.0   # Placeholder
            }
        
        # Calculate approval rate
        total_decided = completed.count()
        approved = completed.filter(status='APPROVED').count()
        
        approval_rate = (approved / total_decided * 100) if total_decided > 0 else 0
        
        # Calculate stagnant applications (no activity for 7+ days)
        seven_days_ago = timezone.now() - timedelta(days=7)
        stagnant = Application.objects.filter(
            status='PROCESSING',
            updated_at__lt=seven_days_ago
        ).count()
        
        return Response({
            'avg_processing_days': avg_processing_days,
            'stage_transition_times': stage_times,
            'approval_rate': approval_rate,
            'stagnant_applications': stagnant,
            'total_completed': total_decided,
            'total_approved': approved,
            'total_rejected': total_decided - approved
        })


class BulkApplicationUpdateView(APIView):
    """
    API endpoint for updating multiple applications at once.
    """
    permission_classes = [IsAuthenticated, IsManager]
    
    def post(self, request):
        application_ids = request.data.get('application_ids', [])
        update_data = request.data.get('update_data', {})
        
        if not application_ids or not update_data:
            return Response({
                'error': 'Both application_ids and update_data are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate allowed fields for bulk update
        allowed_fields = ['status', 'stage', 'assigned_to']
        invalid_fields = [field for field in update_data.keys() if field not in allowed_fields]
        
        if invalid_fields:
            return Response({
                'error': f'Invalid fields for bulk update: {", ".join(invalid_fields)}',
                'allowed_fields': allowed_fields
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get applications to update
        applications = Application.objects.filter(id__in=application_ids)
        found_ids = list(applications.values_list('id', flat=True))
        not_found_ids = [id for id in application_ids if id not in found_ids]
        
        # Update applications
        update_count = applications.update(**update_data)
        
        return Response({
            'message': f'Successfully updated {update_count} applications',
            'updated_ids': found_ids,
            'not_found_ids': not_found_ids,
            'update_data': update_data
        })


class RepaymentReportView(APIView):
    """
    API endpoint for generating repayment reports.
    """
    permission_classes = [IsAuthenticated, IsStaff]
    
    def get(self, request):
        # Get query parameters
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        status = request.query_params.get('status')
        
        # Base queryset
        queryset = Repayment.objects.all()
        
        # Apply filters
        if start_date:
            queryset = queryset.filter(due_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(due_date__lte=end_date)
        if status:
            queryset = queryset.filter(status=status)
        
        # Calculate statistics
        total_repayments = queryset.count()
        total_amount = queryset.aggregate(total=Sum('amount'))['total'] or 0
        paid_amount = queryset.filter(status='PAID').aggregate(total=Sum('amount'))['total'] or 0
        overdue_amount = queryset.filter(status='OVERDUE').aggregate(total=Sum('amount'))['total'] or 0
        
        # Status breakdown
        status_counts = queryset.values('status').annotate(
            count=Count('id'),
            total_amount=Sum('amount')
        ).order_by('status')
        
        # Upcoming repayments (due in the next 30 days)
        today = timezone.now().date()
        thirty_days_later = today + timedelta(days=30)
        upcoming = queryset.filter(
            due_date__gte=today,
            due_date__lte=thirty_days_later,
            status='PENDING'
        ).order_by('due_date')
        
        upcoming_data = []
        for repayment in upcoming:
            upcoming_data.append({
                'id': repayment.id,
                'application_id': repayment.application.id,
                'reference_number': repayment.application.reference_number,
                'borrower_name': repayment.application.borrower.name,
                'amount': repayment.amount,
                'due_date': repayment.due_date,
                'days_until_due': (repayment.due_date - today).days
            })
        
        return Response({
            'total_repayments': total_repayments,
            'total_amount': total_amount,
            'paid_amount': paid_amount,
            'overdue_amount': overdue_amount,
            'payment_rate': (paid_amount / total_amount * 100) if total_amount > 0 else 0,
            'status_breakdown': list(status_counts),
            'upcoming_repayments': upcoming_data
        })
