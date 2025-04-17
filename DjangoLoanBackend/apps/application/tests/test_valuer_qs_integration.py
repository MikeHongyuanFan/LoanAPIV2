import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.application.models import Application
from apps.borrower.models import Borrower
from apps.broker.models import Broker
from apps.product.models import Product


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def sample_borrower():
    return Borrower.objects.create(
        name="Test Borrower",
        email="borrower@example.com",
        phone="1234567890",
        address="123 Test St"
    )


@pytest.fixture
def sample_broker():
    return Broker.objects.create(
        name="Test Broker",
        company="Test Company",
        email="broker@example.com",
        phone="0987654321"
    )


@pytest.fixture
def sample_product():
    return Product.objects.create(
        name="Test Product",
        description="Test Description",
        interest_rate=5.0
    )


@pytest.fixture
def sample_application(sample_borrower, sample_broker, sample_product):
    return Application.objects.create(
        borrower=sample_borrower,
        broker=sample_broker,
        product=sample_product,
        loan_amount=100000,
        loan_term_months=12,
        interest_rate=5.0,
        loan_purpose="PURCHASE",
        property_address="123 Test St",
        property_type="HOUSE",
        property_value=150000,
        stage="ENQUIRY"
    )


@pytest.mark.django_db
def test_valuer_info_serializer(api_client, sample_application):
    """Test that the ValuerInfoSerializer validates correctly"""
    url = reverse('application-update-valuer-info', kwargs={'pk': sample_application.pk})
    
    # Test with valid data
    valid_data = {
        'company_name': 'Test Valuer Company',
        'contact_name': 'John Valuer',
        'email': 'valuer@example.com',
        'phone': '1122334455'
    }
    
    response = api_client.post(url, valid_data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['valuer_info']['company_name'] == 'Test Valuer Company'
    
    # Test with invalid data (missing required field)
    invalid_data = {
        'company_name': 'Test Valuer Company',
        'contact_name': 'John Valuer',
        'phone': '1122334455'
        # Missing email
    }
    
    response = api_client.post(url, invalid_data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'email' in response.data


@pytest.mark.django_db
def test_qs_info_serializer(api_client, sample_application):
    """Test that the QSInfoSerializer validates correctly"""
    url = reverse('application-update-qs-info', kwargs={'pk': sample_application.pk})
    
    # Test with valid data
    valid_data = {
        'company_name': 'Test QS Company',
        'contact_name': 'Jane QS',
        'email': 'qs@example.com',
        'phone': '5544332211'
    }
    
    response = api_client.post(url, valid_data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['qs_info']['company_name'] == 'Test QS Company'
    
    # Test with invalid data (missing required field)
    invalid_data = {
        'company_name': 'Test QS Company',
        'contact_name': 'Jane QS',
        'phone': '5544332211'
        # Missing email
    }
    
    response = api_client.post(url, invalid_data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'email' in response.data


@pytest.mark.django_db
def test_valuer_info_model_methods(sample_application):
    """Test the valuer_info model methods"""
    # Test with no valuer_info
    assert sample_application.get_valuer_info() is None
    
    # Test with valuer_info
    valuer_data = {
        'company_name': 'Test Valuer Company',
        'contact_name': 'John Valuer',
        'email': 'valuer@example.com',
        'phone': '1122334455'
    }
    
    sample_application.valuer_info = valuer_data
    sample_application.save()
    
    assert sample_application.get_valuer_info() == valuer_data


@pytest.mark.django_db
def test_qs_info_model_methods(sample_application):
    """Test the qs_info model methods"""
    # Test with no qs_info
    assert sample_application.get_qs_info() is None
    
    # Test with qs_info
    qs_data = {
        'company_name': 'Test QS Company',
        'contact_name': 'Jane QS',
        'email': 'qs@example.com',
        'phone': '5544332211'
    }
    
    sample_application.qs_info = qs_data
    sample_application.save()
    
    assert sample_application.get_qs_info() == qs_data


@pytest.mark.django_db
def test_application_serializer_validation(api_client, sample_application):
    """Test that the ApplicationSerializer validates valuer_info and qs_info correctly"""
    url = reverse('application-detail', kwargs={'pk': sample_application.pk})
    
    # Set application to VALUATION stage
    sample_application.stage = 'VALUATION'
    sample_application.save()
    
    # Test with missing valuer_info
    data = {
        'valuer_info': None
    }
    
    response = api_client.patch(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'valuer_info' in response.data
    
    # Set application to DUAL stage
    sample_application.stage = 'DUAL'
    sample_application.save()
    
    # Test with missing qs_info
    data = {
        'qs_info': None
    }
    
    response = api_client.patch(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'qs_info' in response.data
