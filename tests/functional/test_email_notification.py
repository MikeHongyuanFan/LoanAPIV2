import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.utils import timezone
from decimal import Decimal
import json

from apps.notification.models import NotificationTemplate, Notification
from apps.application.models import Application
from apps.borrower.models import Borrower
from apps.authentication.models import UserProfile
from django.contrib.auth.models import User
from apps.product.models import Product


@pytest.mark.django_db
class TestEmailNotification:
    """
    Test email notification functionality
    """
    
    @pytest.fixture
    def api_client(self):
        return APIClient()
    
    @pytest.fixture
    def admin_user(self):
        user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpassword',
            is_staff=True
        )
        UserProfile.objects.create(
            user=user,
            phone='1234567890',
            position='Administrator',
            department='IT'
        )
        return user
    
    @pytest.fixture
    def admin_client(self, admin_user):
        client = APIClient()
        client.force_authenticate(user=admin_user)
        return client
    
    @pytest.fixture
    def borrower(self):
        return Borrower.objects.create(
            name="John Doe",
            email="john.doe@example.com",
            phone="1234567890",
            address="123 Test St, Test City",
            date_of_birth="1980-01-01",
            gender="M",
            id_number="ABC123456",
            id_type="Passport",
            employment_status="EMPLOYED",
            employer="Test Company",
            income=Decimal("75000.00")
        )
    
    @pytest.fixture
    def product(self):
        return Product.objects.create(
            name="Standard Loan",
            description="Standard loan product",
            loan_type="STANDARD",
            min_loan_amount=Decimal("50000.00"),
            max_loan_amount=Decimal("1000000.00"),
            min_interest_rate=Decimal("4.5"),
            max_interest_rate=Decimal("7.5"),
            min_term_months=12,
            max_term_months=360,
            establishment_fee=Decimal("1500.00"),
            active=True
        )
    
    @pytest.fixture
    def application(self, borrower, product):
        return Application.objects.create(
            borrower=borrower,
            reference_number="APP-202504-TEST1",
            status="SUBMITTED",
            loan_amount=Decimal("250000.00"),
            loan_term_months=30,
            interest_rate=Decimal("5.25"),
            loan_purpose="PURCHASE",
            property_address="123 Test Street, Test City",
            property_value=Decimal("500000.00"),
            property_type="HOUSE",
            application_date=timezone.now().date(),
            product=product
        )
    
    @pytest.fixture
    def notification_template(self):
        return NotificationTemplate.objects.create(
            type="STAGE_CHANGE",
            name="Application Stage Change",
            subject_template="Application {{ reference_number }} status changed to {{ stage }}",
            body_template="""
            Dear {{ borrower_name }},
            
            Your loan application ({{ reference_number }}) status has been updated to {{ stage }}.
            
            Loan Amount: {{ loan_amount }}
            Interest Rate: {{ interest_rate }}%
            Property Address: {{ property_address }}
            
            If you have any questions, please contact us at {{ support_email }}.
            
            Regards,
            {{ company_name }}
            """
        )
    
    def test_send_email_with_application_data(self, admin_client, application, notification_template):
        """
        Test sending an email notification using application data
        """
        url = reverse('send-email-notification')
        
        data = {
            'template_id': notification_template.id,
            'application_id': application.id,
            'recipient_email': 'test@example.com'
        }
        
        response = admin_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'notification_id' in response.data
        
        # Verify the notification was created
        notification_id = response.data['notification_id']
        notification = Notification.objects.get(id=notification_id)
        
        # Check that application data was properly included
        assert application.reference_number in notification.subject
        assert application.get_status_display() in notification.subject
        assert application.borrower.name in notification.message
        assert application.reference_number in notification.message
        assert str(application.loan_amount) in notification.message
        assert str(application.interest_rate) in notification.message
        assert application.property_address in notification.message
    
    def test_send_email_with_custom_data(self, admin_client, notification_template):
        """
        Test sending an email notification with custom data
        """
        url = reverse('send-email-notification')
        
        custom_data = {
            'reference_number': 'APP-CUSTOM-123',
            'stage': 'Custom Stage',
            'borrower_name': 'Custom Borrower',
            'loan_amount': '$300,000.00',
            'interest_rate': '4.5',
            'property_address': 'Custom Address',
            'support_email': 'custom@example.com',
            'company_name': 'Custom Company'
        }
        
        data = {
            'template_id': notification_template.id,
            'recipient_email': 'test@example.com',
            'custom_data': custom_data
        }
        
        response = admin_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'notification_id' in response.data
        
        # Verify the notification was created
        notification_id = response.data['notification_id']
        notification = Notification.objects.get(id=notification_id)
        
        # Check that custom data was properly included
        assert custom_data['reference_number'] in notification.subject
        assert custom_data['stage'] in notification.subject
        assert custom_data['borrower_name'] in notification.message
        assert custom_data['reference_number'] in notification.message
        assert custom_data['loan_amount'] in notification.message
        assert custom_data['interest_rate'] in notification.message
        assert custom_data['property_address'] in notification.message
        assert custom_data['support_email'] in notification.message
        assert custom_data['company_name'] in notification.message
    
    def test_preview_template_with_application_data(self, admin_client, application, notification_template):
        """
        Test previewing a template with application data
        """
        url = reverse('notification-template-preview')
        
        data = {
            'template_id': notification_template.id,
            'application_id': application.id
        }
        
        response = admin_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'subject' in response.data
        assert 'body' in response.data
        
        # Check that application data was properly included
        assert application.reference_number in response.data['subject']
        assert application.get_status_display() in response.data['subject']
        assert application.borrower.name in response.data['body']
        assert application.reference_number in response.data['body']
        assert str(application.loan_amount) in response.data['body']
        assert str(application.interest_rate) in response.data['body']
        assert application.property_address in response.data['body']
