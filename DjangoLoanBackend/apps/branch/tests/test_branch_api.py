import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.branch.models import Branch


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


@pytest.mark.django_db
def test_create_branch(api_client):
    """Test creating a branch"""
    url = reverse('branch-list')
    data = {
        'name': 'New Branch',
        'code': 'NB001',
        'address_line1': '456 New St',
        'city': 'New City',
        'state': 'New State',
        'postal_code': '54321',
        'country': 'Australia',
        'phone': '0987654321',
        'email': 'newbranch@example.com'
    }
    
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Branch.objects.count() == 1
    assert Branch.objects.get().name == 'New Branch'


@pytest.mark.django_db
def test_get_branch_list(api_client, sample_branch):
    """Test getting a list of branches"""
    url = reverse('branch-list')
    response = api_client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'Test Branch'


@pytest.mark.django_db
def test_get_branch_detail(api_client, sample_branch):
    """Test getting branch details"""
    url = reverse('branch-detail', kwargs={'pk': sample_branch.pk})
    response = api_client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == 'Test Branch'
    assert response.data['code'] == 'TB001'
    assert 'full_address' in response.data
    assert 'bd_count' in response.data


@pytest.mark.django_db
def test_update_branch(api_client, sample_branch):
    """Test updating a branch"""
    url = reverse('branch-detail', kwargs={'pk': sample_branch.pk})
    data = {
        'name': 'Updated Branch',
        'manager_name': 'John Manager'
    }
    
    response = api_client.patch(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    
    sample_branch.refresh_from_db()
    assert sample_branch.name == 'Updated Branch'
    assert sample_branch.manager_name == 'John Manager'


@pytest.mark.django_db
def test_delete_branch(api_client, sample_branch):
    """Test deleting a branch"""
    url = reverse('branch-detail', kwargs={'pk': sample_branch.pk})
    response = api_client.delete(url)
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Branch.objects.count() == 0


@pytest.mark.django_db
def test_active_branches(api_client):
    """Test getting active branches"""
    Branch.objects.create(
        name="Active Branch",
        code="AB001",
        address_line1="123 Active St",
        city="Active City",
        state="Active State",
        postal_code="12345",
        country="Australia",
        phone="1234567890",
        email="active@example.com",
        is_active=True
    )
    
    Branch.objects.create(
        name="Inactive Branch",
        code="IB001",
        address_line1="123 Inactive St",
        city="Inactive City",
        state="Inactive State",
        postal_code="54321",
        country="Australia",
        phone="0987654321",
        email="inactive@example.com",
        is_active=False
    )
    
    url = reverse('branch-active')
    response = api_client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'Active Branch'
