import pytest
from django.urls import reverse
from rest_framework import status
from django.utils import timezone
from apps.application.models import Fee, Payment, Note

@pytest.mark.django_db
class TestFeeManagement:
    """
    Test the fee management functionality
    """
    
    def test_create_fee(self, admin_client, application):
        """
        Test creating a fee
        """
        fee_url = reverse('fee-list')
        fee_data = {
            'application': application.id,
            'fee_type': 'ESTABLISHMENT',
            'description': 'Establishment Fee',
            'amount': 1500.00,
            'due_date': timezone.now().date().isoformat()
        }
        
        response = admin_client.post(fee_url, fee_data)
        assert response.status_code == status.HTTP_201_CREATED
        
        # Verify the fee was created
        fee_id = response.data['id']
        fee = Fee.objects.get(id=fee_id)
        assert fee.fee_type == 'ESTABLISHMENT'
        assert fee.amount == 1500.00
        assert fee.status == 'PENDING'
        
    def test_mark_fee_as_paid(self, admin_client, application):
        """
        Test marking a fee as paid
        """
        # First create a fee
        fee = Fee.objects.create(
            application=application,
            fee_type='LEGAL',
            description='Legal Fee',
            amount=750.00,
            status='PENDING',
            due_date=timezone.now().date()
        )
        
        # Mark the fee as paid
        mark_paid_url = reverse('fee-mark-as-paid', args=[fee.id])
        payment_data = {
            'payment_method': 'BANK_TRANSFER',
            'reference': 'REF123456'
        }
        
        response = admin_client.post(mark_paid_url, payment_data)
        assert response.status_code == status.HTTP_200_OK
        
        # Verify the fee status was updated
        fee.refresh_from_db()
        assert fee.status == 'PAID'
        
        # Verify a payment was created
        payment = Payment.objects.filter(application=application).first()
        assert payment is not None
        assert payment.amount == fee.amount
        assert payment.payment_method == 'BANK_TRANSFER'
        assert payment.reference == 'REF123456'
        
    def test_waive_fee(self, admin_client, application):
        """
        Test waiving a fee
        """
        # First create a fee
        fee = Fee.objects.create(
            application=application,
            fee_type='PROCESSING',
            description='Processing Fee',
            amount=250.00,
            status='PENDING',
            due_date=timezone.now().date()
        )
        
        # Waive the fee
        waive_url = reverse('fee-waive', args=[fee.id])
        waive_data = {
            'reason': 'Goodwill gesture for loyal customer'
        }
        
        response = admin_client.post(waive_url, waive_data)
        assert response.status_code == status.HTTP_200_OK
        
        # Verify the fee status was updated
        fee.refresh_from_db()
        assert fee.status == 'WAIVED'
        
        # Verify a note was created
        note = Note.objects.filter(application=application).first()
        assert note is not None
        assert 'Fee waived' in note.content
        assert 'Goodwill gesture for loyal customer' in note.content
