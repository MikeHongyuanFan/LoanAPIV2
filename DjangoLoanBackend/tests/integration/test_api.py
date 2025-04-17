"""
Integration tests for API endpoints in the Loan Application System.
"""

import pytest
import json
from django.urls import reverse
from rest_framework import status
from apps.borrower.models import Borrower
from apps.broker.models import Broker
from apps.product.models import Product

@pytest.mark.django_db
class TestBorrowerAPI:
    """Test cases for the Borrower API endpoints."""
    
    def test_list_borrowers(self, admin_client):
        """Test that borrowers can be listed."""
        url = reverse('borrower-list')
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
    
    def test_create_borrower(self, admin_client):
        """Test that a borrower can be created."""
        url = reverse('borrower-list')
        data = {
            'name': 'New Borrower',
            'email': 'new@example.com',
            'phone': '9876543210',
            'address': '789 New St, New City',
            'date_of_birth': '1990-01-01',
            'gender': 'F',
            'id_number': 'ID67890',
            'id_type': 'Driver License',
            'employment_status': 'EMPLOYED',
            'employer': 'New Company',
            'income': 60000.00
        }
        response = admin_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Borrower.objects.filter(name='New Borrower').exists()
    
    def test_retrieve_borrower(self, admin_client, borrower):
        """Test that a borrower can be retrieved."""
        url = reverse('borrower-detail', args=[borrower.id])
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == borrower.name
    
    def test_update_borrower(self, admin_client, borrower):
        """Test that a borrower can be updated."""
        url = reverse('borrower-detail', args=[borrower.id])
        data = {'name': 'Updated Borrower Name'}
        response = admin_client.patch(
            url, 
            data=json.dumps(data),
            content_type='application/json'
        )
        assert response.status_code == status.HTTP_200_OK
        borrower.refresh_from_db()
        assert borrower.name == 'Updated Borrower Name'
    
    def test_delete_borrower(self, admin_client, borrower):
        """Test that a borrower can be deleted."""
        url = reverse('borrower-detail', args=[borrower.id])
        response = admin_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Borrower.objects.filter(id=borrower.id).exists()


@pytest.mark.django_db
class TestBrokerAPI:
    """Test cases for the Broker API endpoints."""
    
    def test_list_brokers(self, admin_client):
        """Test that brokers can be listed."""
        url = reverse('broker-list')
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
    
    def test_create_broker(self, admin_client):
        """Test that a broker can be created."""
        url = reverse('broker-list')
        data = {
            'name': 'New Broker',
            'email': 'newbroker@example.com',
            'phone': '1122334455',
            'company': 'New Brokerage',
            'address': '101 Broker Ave, Broker Town',
            'license_number': 'BRK67890',
            'commission_rate': 3.0
        }
        response = admin_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Broker.objects.filter(name='New Broker').exists()


@pytest.mark.django_db
class TestProductAPI:
    """Test cases for the Product API endpoints."""
    
    def test_list_products(self, admin_client):
        """Test that products can be listed."""
        url = reverse('product-list')
        response = admin_client.get(url)
        assert response.status_code == status.HTTP_200_OK
    
    def test_create_product(self, admin_client):
        """Test that a product can be created."""
        url = reverse('product-list')
        data = {
            'name': 'New Loan Product',
            'description': 'A new test loan product',
            'loan_type': 'PERSONAL',
            'min_loan_amount': 5000.00,
            'max_loan_amount': 50000.00,
            'min_interest_rate': 5.0,
            'max_interest_rate': 15.0,
            'min_term_months': 6,
            'max_term_months': 60,
            'establishment_fee': 500.00
        }
        response = admin_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Product.objects.filter(name='New Loan Product').exists()
