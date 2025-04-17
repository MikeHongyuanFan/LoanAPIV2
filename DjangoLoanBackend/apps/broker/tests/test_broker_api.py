import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.broker.models import Broker, BrokerTier, BrokerSpecialization
from apps.branch.models import Branch
from apps.bd.models import BD
import datetime


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def sample_branch():
    return Branch.objects.create(
        name="Test Branch",
        code="TB001",
        address_line1="123 Test St",
        city="Test City",
        state="Test State",
        postal_code="12345",
        country="Australia",
        phone="1234567890",
        email="branch@example.com"
    )


@pytest.fixture
def sample_bd(sample_branch):
    return BD.objects.create(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        phone="1234567890",
        branch=sample_branch,
        employee_id="EMP001",
        position="Business Development Manager",
        hire_date=datetime.date(2020, 1, 1),
        is_active=True
    )


@pytest.fixture
def sample_tier():
    return BrokerTier.objects.create(
        name="Gold",
        description="Gold tier brokers",
        commission_multiplier=1.5
    )


@pytest.fixture
def sample_specialization():
    return BrokerSpecialization.objects.create(
        name="Residential",
        description="Residential property loans"
    )


@pytest.fixture
def sample_broker(sample_branch, sample_bd, sample_tier):
    broker = Broker.objects.create(
        name="Test Broker",
        email="broker@example.com",
        phone="1234567890",
        company="Test Company",
        address="123 Broker St",
        license_number="LIC123",
        commission_rate=5.0,
        active=True,
        branch=sample_branch,
        bd=sample_bd,
        tier=sample_tier,
        years_of_experience=5,
        accreditation_number="ACC123",
        accreditation_expiry=datetime.date(2025, 1, 1)
    )
    return broker


@pytest.mark.django_db
def test_create_broker(api_client, sample_branch, sample_bd, sample_tier, sample_specialization):
    """Test creating a broker with branch, BD, tier, and specialization"""
    url = reverse('broker-list')
    data = {
        'name': 'New Broker',
        'email': 'newbroker@example.com',
        'phone': '0987654321',
        'company': 'New Company',
        'address': '456 New St',
        'license_number': 'LIC456',
        'commission_rate': 4.5,
        'active': True,
        'branch': str(sample_branch.id),
        'bd': str(sample_bd.id),
        'tier': str(sample_tier.id),
        'specializations': [str(sample_specialization.id)],
        'years_of_experience': 3,
        'accreditation_number': 'ACC456',
        'accreditation_expiry': '2024-06-30'
    }
    
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Broker.objects.count() == 1
    
    broker = Broker.objects.get()
    assert broker.name == 'New Broker'
    assert broker.branch == sample_branch
    assert broker.bd == sample_bd
    assert broker.tier == sample_tier
    assert list(broker.specializations.all()) == [sample_specialization]


@pytest.mark.django_db
def test_get_broker_list(api_client, sample_broker):
    """Test getting a list of brokers"""
    url = reverse('broker-list')
    response = api_client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'Test Broker'
    assert response.data[0]['branch_name'] == 'Test Branch'
    assert response.data[0]['bd_name'] == 'John Doe'
    assert response.data[0]['tier_name'] == 'Gold'


@pytest.mark.django_db
def test_get_broker_detail(api_client, sample_broker, sample_specialization):
    """Test getting broker details"""
    sample_broker.specializations.add(sample_specialization)
    
    url = reverse('broker-detail', kwargs={'pk': sample_broker.pk})
    response = api_client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == 'Test Broker'
    assert response.data['branch_name'] == 'Test Branch'
    assert response.data['bd_name'] == 'John Doe'
    assert response.data['tier_name'] == 'Gold'
    assert response.data['specialization_names'] == ['Residential']
    assert response.data['accreditation_valid'] == True


@pytest.mark.django_db
def test_update_broker(api_client, sample_broker, sample_specialization):
    """Test updating a broker"""
    url = reverse('broker-detail', kwargs={'pk': sample_broker.pk})
    data = {
        'name': 'Updated Broker',
        'years_of_experience': 8,
        'specializations': [str(sample_specialization.id)]
    }
    
    response = api_client.patch(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    
    sample_broker.refresh_from_db()
    assert sample_broker.name == 'Updated Broker'
    assert sample_broker.years_of_experience == 8
    assert list(sample_broker.specializations.all()) == [sample_specialization]


@pytest.mark.django_db
def test_delete_broker(api_client, sample_broker):
    """Test deleting a broker"""
    url = reverse('broker-detail', kwargs={'pk': sample_broker.pk})
    response = api_client.delete(url)
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Broker.objects.count() == 0


@pytest.mark.django_db
def test_active_brokers(api_client, sample_branch, sample_bd, sample_tier):
    """Test getting active brokers"""
    Broker.objects.create(
        name="Active Broker",
        email="active@example.com",
        phone="1234567890",
        company="Active Company",
        address="123 Active St",
        license_number="LIC123",
        commission_rate=5.0,
        active=True,
        branch=sample_branch,
        bd=sample_bd,
        tier=sample_tier
    )
    
    Broker.objects.create(
        name="Inactive Broker",
        email="inactive@example.com",
        phone="0987654321",
        company="Inactive Company",
        address="456 Inactive St",
        license_number="LIC456",
        commission_rate=4.5,
        active=False,
        branch=sample_branch,
        bd=sample_bd,
        tier=sample_tier
    )
    
    url = reverse('broker-active')
    response = api_client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'Active Broker'


@pytest.mark.django_db
def test_brokers_by_branch(api_client, sample_broker):
    """Test getting brokers grouped by branch"""
    url = reverse('broker-by-branch')
    response = api_client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'Test Branch'
    assert len(response.data[0]['brokers']) == 1
    assert response.data[0]['brokers'][0]['name'] == 'Test Broker'


@pytest.mark.django_db
def test_brokers_by_bd(api_client, sample_broker):
    """Test getting brokers grouped by BD"""
    url = reverse('broker-by-bd')
    response = api_client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['full_name'] == 'John Doe'
    assert len(response.data[0]['brokers']) == 1
    assert response.data[0]['brokers'][0]['name'] == 'Test Broker'


@pytest.mark.django_db
def test_brokers_by_tier(api_client, sample_broker):
    """Test getting brokers grouped by tier"""
    url = reverse('broker-by-tier')
    response = api_client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'Gold'
    assert len(response.data[0]['brokers']) == 1
    assert response.data[0]['brokers'][0]['name'] == 'Test Broker'
