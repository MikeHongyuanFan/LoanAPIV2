import pytest
from django.urls import reverse
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from apps.application.models import Extension
from apps.notification.models import Notification

@pytest.mark.django_db
class TestLoanExtension:
    """
    Test the loan extension functionality
    """
    
    def test_create_extension_request(self, admin_client, application):
        """
        Test creating a loan extension request
        """
        # Set an expiry date for the application
        application.expiry_date = timezone.now().date() + timedelta(days=30)
        application.save()
        
        extension_url = reverse('extension-list')
        new_expiry_date = (application.expiry_date + timedelta(days=90)).isoformat()
        
        extension_data = {
            'application': application.id,
            'original_expiry_date': application.expiry_date.isoformat(),
            'new_expiry_date': new_expiry_date,
            'reason': 'Client needs additional time to complete project',
            'status': 'PENDING',  # Add status explicitly
            'requested_date': timezone.now().date().isoformat()  # Add requested_date explicitly
        }
        
        response = admin_client.post(extension_url, extension_data, format='json')  # Use format='json' to avoid QueryDict issues
        assert response.status_code == status.HTTP_201_CREATED
        
        # Verify the extension was created
        extension_id = response.data['id']
        extension = Extension.objects.get(id=extension_id)
        assert extension.status == 'PENDING'
        assert extension.reason == 'Client needs additional time to complete project'
        
        # Verify a notification was created
        notifications = Notification.objects.filter(
            type='EXTENSION_REQUEST',
            related_id=extension.id
        )
        assert notifications.exists()
        
    def test_approve_extension(self, admin_client, application):
        """
        Test approving a loan extension
        """
        # Set an expiry date for the application
        original_expiry = timezone.now().date() + timedelta(days=30)
        application.expiry_date = original_expiry
        application.save()
        
        # Create an extension request
        extension = Extension.objects.create(
            application=application,
            requested_date=timezone.now().date(),
            original_expiry_date=original_expiry,
            new_expiry_date=original_expiry + timedelta(days=60),
            reason='Need more time due to construction delays',
            status='PENDING'
        )
        
        # Approve the extension
        approve_url = reverse('extension-approve', args=[extension.id])
        response = admin_client.post(approve_url)
        assert response.status_code == status.HTTP_200_OK
        
        # Verify the extension status was updated
        extension.refresh_from_db()
        assert extension.status == 'APPROVED'
        
        # Verify the application expiry date was updated
        application.refresh_from_db()
        assert application.expiry_date == extension.new_expiry_date
        
        # Verify notifications were created
        notifications = Notification.objects.filter(
            type='EXTENSION_STATUS',
            related_id=extension.id
        )
        assert notifications.exists()
        
    def test_decline_extension(self, admin_client, application):
        """
        Test declining a loan extension
        """
        # Set an expiry date for the application
        original_expiry = timezone.now().date() + timedelta(days=30)
        application.expiry_date = original_expiry
        application.save()
        
        # Create an extension request
        extension = Extension.objects.create(
            application=application,
            requested_date=timezone.now().date(),
            original_expiry_date=original_expiry,
            new_expiry_date=original_expiry + timedelta(days=90),
            reason='Need more time to sell property',
            status='PENDING'
        )
        
        # Decline the extension
        decline_url = reverse('extension-decline', args=[extension.id])
        response = admin_client.post(decline_url)
        assert response.status_code == status.HTTP_200_OK
        
        # Verify the extension status was updated
        extension.refresh_from_db()
        assert extension.status == 'DECLINED'
        
        # Verify the application expiry date was NOT updated
        application.refresh_from_db()
        assert application.expiry_date == original_expiry
