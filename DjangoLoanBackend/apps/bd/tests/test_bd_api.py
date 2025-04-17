import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.bd.models import BD
from apps.branch.models import Branch
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


@pytest.mark.django_db
def test_create_bd(api_client, sample_branch):
    """Test creating a BD"""
    url = reverse('bd-list')
    data = {
        'first_name': 'Jane',
        'last_name': 'Smith',
        'email': 'jane.smith@example.com',
        'phone': '0987654321',
        'branch': str(sample_branch.id),
        'employee_id': 'EMP002',
        'position': 'Senior Business Developer',
        'hire_date': '2021-02-15',
        'is_active': True
    }
    
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert BD.objects.count() == 1
    assert BD.objects.get().email == 'jane.smith@example.com'


@pytest.mark.django_db
def test_get_bd_list(api_client, sample_bd):
    """Test getting a list of BDs"""
    url = reverse('bd-list')
    response = api_client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['full_name'] == 'John Doe'


@pytest.mark.django_db
def test_get_bd_detail(api_client, sample_bd):
    """Test getting BD details"""
    url = reverse('bd-detail', kwargs={'pk': sample_bd.pk})
    response = api_client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data['first_name'] == 'John'
    assert response.data['last_name'] == 'Doe'
    assert response.data['full_name'] == 'John Doe'
    assert response.data['branch_name'] == 'Test Branch'
    assert 'experience_years' in response.data
    assert 'branch_details' in response.data


@pytest.mark.django_db
def test_update_bd(api_client, sample_bd):
    """Test updating a BD"""
    url = reverse('bd-detail', kwargs={'pk': sample_bd.pk})
    data = {
        'first_name': 'Johnny',
        'position': 'Senior Business Development Manager'
    }
    
    response = api_client.patch(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    
    sample_bd.refresh_from_db()
    assert sample_bd.first_name == 'Johnny'
    assert sample_bd.position == 'Senior Business Development Manager'


@pytest.mark.django_db
def test_delete_bd(api_client, sample_bd):
    """Test deleting a BD"""
    url = reverse('bd-detail', kwargs={'pk': sample_bd.pk})
    response = api_client.delete(url)
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert BD.objects.count() == 0


@pytest.mark.django_db
def test_active_bds(api_client, sample_branch):
    """Test getting active BDs"""
    BD.objects.create(
        first_name="Active",
        last_name="User",
        email="active@example.com",
        phone="1234567890",
        branch=sample_branch,
        employee_id="EMP001",
        position="Business Developer",
        hire_date=datetime.date(2020, 1, 1),
        is_active=True
    )
    
    BD.objects.create(
        first_name="Inactive",
        last_name="User",
        email="inactive@example.com",
        phone="0987654321",
        branch=sample_branch,
        employee_id="EMP002",
        position="Business Developer",
        hire_date=datetime.date(2020, 1, 1),
        is_active=False
    )
    
    url = reverse('bd-active')
    response = api_client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['full_name'] == 'Active User'


@pytest.mark.django_db
def test_by_branch(api_client, sample_branch):
    """Test getting BDs grouped by branch"""
    branch2 = Branch.objects.create(
        name="Second Branch",
        code="SB001",
        address_line1="456 Second St",
        city="Second City",
        state="Second State",
        postal_code="54321",
        country="Australia",
        phone="0987654321",
        email="second@example.com"
    )
    
    BD.objects.create(
        first_name="First",
        last_name="BD",
        email="first@example.com",
        phone="1234567890",
        branch=sample_branch,
        employee_id="EMP001",
        position="Business Developer",
        hire_date=datetime.date(2020, 1, 1),
        is_active=True
    )
    
    BD.objects.create(
        first_name="Second",
        last_name="BD",
        email="second@example.com",
        phone="0987654321",
        branch=branch2,
        employee_id="EMP002",
        position="Business Developer",
        hire_date=datetime.date(2020, 1, 1),
        is_active=True
    )
    
    url = reverse('bd-by-branch')
    response = api_client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    
    # Check that each branch has the correct BDs
    for branch_data in response.data:
        if branch_data['name'] == 'Test Branch':
            assert len(branch_data['bds']) == 1
            assert branch_data['bds'][0]['full_name'] == 'First BD'
        elif branch_data['name'] == 'Second Branch':
            assert len(branch_data['bds']) == 1
            assert branch_data['bds'][0]['full_name'] == 'Second BD'
