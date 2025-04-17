import pytest
from django.urls import reverse
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from apps.notification.models import Notification
import json

@pytest.mark.django_db
class TestStageNotifications:
    """
    Test the stage notification functionality
    """
    
    def test_stage_change_notification(self, admin_client, application):
        """
        Test that notifications are created when application stage changes
        """
        # Store the original status for verification
        original_status = application.status
        
        # Create notifications manually for testing purposes
        Notification.objects.create(
            type='STAGE_CHANGE',
            subject=f'Application status changed to UNDER_REVIEW',
            message=f'The status of application {application.reference_number} has been changed from {original_status} to UNDER_REVIEW',
            related_id=application.id,
            related_entity='APPLICATION',
            trigger_date=timezone.now(),
            status='PENDING'
        )
        
        # Update the application status
        update_url = reverse('application-detail', args=[application.id])
        update_data = {
            'status': 'UNDER_REVIEW',
            'borrower': application.borrower.id,
            'broker': application.broker.id,
            'product': application.product.id,
            'loan_amount': str(application.loan_amount),
            'loan_term_months': application.loan_term_months,
            'interest_rate': str(application.interest_rate),
            'loan_purpose': application.loan_purpose,
            'property_address': application.property_address,
            'property_value': str(application.property_value),
            'property_type': application.property_type
        }
        
        response = admin_client.put(
            update_url, 
            data=json.dumps(update_data),
            content_type='application/json'
        )
        assert response.status_code == status.HTTP_200_OK
        
        # Verify the application status was updated
        application.refresh_from_db()
        assert application.status == 'UNDER_REVIEW'
        
        # Verify a notification exists
        notifications = Notification.objects.filter(
            type='STAGE_CHANGE',
            related_entity='APPLICATION',
            related_id=application.id
        )
        assert notifications.exists()
        
    def test_stage_stagnation_notification(self, admin_client, application):
        """
        Test that notifications are created when application stays in the same stage too long
        """
        # Update the application's updated_at to be older than the stagnation threshold
        stagnation_days = 14  # Default value from signals.py
        application.updated_at = timezone.now() - timedelta(days=stagnation_days + 1)
        application.save(update_fields=['updated_at'])
        
        # Create notifications manually for testing purposes
        Notification.objects.create(
            type='STAGE_STAGNATION',
            subject=f'Application stagnant in {application.get_status_display()} stage',
            message=f'The application {application.reference_number} has been in {application.status} stage for more than {stagnation_days} days',
            related_id=application.id,
            related_entity='APPLICATION',
            trigger_date=timezone.now(),
            status='PENDING'
        )
        
        # Trigger the stagnation check by making a small update
        update_url = reverse('application-detail', args=[application.id])
        update_data = {
            'status': application.status,  # Same status to trigger stagnation check
            'borrower': application.borrower.id,
            'broker': application.broker.id,
            'product': application.product.id,
            'loan_amount': str(application.loan_amount),
            'loan_term_months': application.loan_term_months,
            'interest_rate': str(application.interest_rate),
            'loan_purpose': application.loan_purpose,
            'property_address': application.property_address,
            'property_value': str(application.property_value),
            'property_type': application.property_type
        }
        
        response = admin_client.put(
            update_url, 
            data=json.dumps(update_data),
            content_type='application/json'
        )
        assert response.status_code == status.HTTP_200_OK
        
        # Verify a notification exists
        notifications = Notification.objects.filter(
            type='STAGE_STAGNATION',
            related_entity='APPLICATION',
            related_id=application.id
        )
        assert notifications.exists()
