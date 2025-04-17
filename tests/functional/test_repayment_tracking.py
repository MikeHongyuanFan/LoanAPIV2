import pytest
from django.urls import reverse
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from apps.application.models import Repayment, Payment
from apps.notification.models import Notification

@pytest.mark.django_db
class TestRepaymentTracking:
    """
    Test the repayment tracking functionality
    """
    
    def test_create_repayment(self, admin_client, application):
        """
        Test creating a repayment
        """
        repayment_url = reverse('repayment-list')
        due_date = (timezone.now() + timedelta(days=30)).date().isoformat()
        
        repayment_data = {
            'application': application.id,
            'due_date': due_date,
            'amount': 5000.00,
            'principal_amount': 4500.00,
            'interest_amount': 500.00
        }
        
        response = admin_client.post(repayment_url, repayment_data)
        assert response.status_code == status.HTTP_201_CREATED
        
        # Verify the repayment was created
        repayment_id = response.data['id']
        repayment = Repayment.objects.get(id=repayment_id)
        assert repayment.amount == 5000.00
        assert repayment.status == 'SCHEDULED'
        
        # Verify notifications were created
        notifications = Notification.objects.filter(
            type='REPAYMENT_REMINDER',
            related_id=repayment.id
        )
        assert notifications.exists()
        
    def test_record_partial_payment(self, admin_client, application):
        """
        Test recording a partial payment for a repayment
        """
        # First create a repayment
        repayment = Repayment.objects.create(
            application=application,
            due_date=timezone.now().date() + timedelta(days=15),
            amount=10000.00,
            principal_amount=9000.00,
            interest_amount=1000.00,
            status='SCHEDULED'
        )
        
        # Record a partial payment
        payment_url = reverse('repayment-record-payment', args=[repayment.id])
        payment_data = {
            'amount': 5000.00,
            'payment_method': 'BANK_TRANSFER',
            'reference': 'PARTIAL123'
        }
        
        response = admin_client.post(payment_url, payment_data)
        assert response.status_code == status.HTTP_200_OK
        
        # Verify the repayment status was updated
        repayment.refresh_from_db()
        assert repayment.status == 'PARTIAL'
        assert repayment.paid_amount == 5000.00
        
        # Verify a payment was created
        payment = Payment.objects.filter(application=application).first()
        assert payment is not None
        assert payment.amount == 5000.00
        assert payment.payment_method == 'BANK_TRANSFER'
        
    def test_record_full_payment(self, admin_client, application):
        """
        Test recording a full payment for a repayment
        """
        # First create a repayment
        repayment = Repayment.objects.create(
            application=application,
            due_date=timezone.now().date() + timedelta(days=15),
            amount=7500.00,
            principal_amount=7000.00,
            interest_amount=500.00,
            status='SCHEDULED'
        )
        
        # Record a full payment
        payment_url = reverse('repayment-record-payment', args=[repayment.id])
        payment_data = {
            'amount': 7500.00,
            'payment_method': 'DIRECT_DEBIT',
            'reference': 'FULL123'
        }
        
        response = admin_client.post(payment_url, payment_data)
        assert response.status_code == status.HTTP_200_OK
        
        # Verify the repayment status was updated
        repayment.refresh_from_db()
        assert repayment.status == 'PAID'
        assert repayment.paid_amount == 7500.00
        assert repayment.paid_date is not None
