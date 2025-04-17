import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.company.models import Company, Director, Shareholder, FinancialInformation
import datetime
from decimal import Decimal


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def sample_company():
    return Company.objects.create(
        name="Test Company Pty Ltd",
        trading_name="Test Company",
        company_type="PTY_LTD",
        acn="123456789",
        abn="12345678901",
        registration_date=datetime.date(2010, 1, 1),
        registration_jurisdiction="NSW",
        registered_address_line1="123 Registered St",
        registered_city="Sydney",
        registered_state="NSW",
        registered_postal_code="2000",
        registered_country="Australia",
        business_address_line1="456 Business St",
        business_city="Sydney",
        business_state="NSW",
        business_postal_code="2000",
        business_country="Australia",
        phone="0298765432",
        email="info@testcompany.com.au",
        website="https://www.testcompany.com.au",
        industry="Technology",
        business_description="Software development",
        employees_count=25,
        years_in_business=13
    )


@pytest.fixture
def sample_director(sample_company):
    return Director.objects.create(
        company=sample_company,
        first_name="John",
        last_name="Smith",
        date_of_birth=datetime.date(1975, 5, 15),
        director_id="DIR123456",
        appointment_date=datetime.date(2010, 1, 1),
        role="MANAGING_DIRECTOR",
        residential_address_line1="789 Home St",
        residential_city="Sydney",
        residential_state="NSW",
        residential_postal_code="2000",
        residential_country="Australia",
        phone="0412345678",
        email="john.smith@testcompany.com.au",
        identification_type="DRIVERS_LICENSE",
        identification_number="DL123456"
    )


@pytest.fixture
def sample_shareholder(sample_company, sample_director):
    return Shareholder.objects.create(
        company=sample_company,
        shareholder_type="INDIVIDUAL",
        individual_first_name="John",
        individual_last_name="Smith",
        individual_date_of_birth=datetime.date(1975, 5, 15),
        shareholding_percentage=Decimal("60.0"),
        share_class="ORDINARY",
        acquisition_date=datetime.date(2010, 1, 1),
        is_director=True,
        director=sample_director
    )


@pytest.fixture
def sample_financial(sample_company):
    return FinancialInformation.objects.create(
        company=sample_company,
        financial_year="2022",
        financial_year_end_date=datetime.date(2022, 6, 30),
        annual_revenue=Decimal("5000000.00"),
        annual_profit=Decimal("750000.00"),
        total_assets=Decimal("3000000.00"),
        total_liabilities=Decimal("1500000.00"),
        current_assets=Decimal("1200000.00"),
        current_liabilities=Decimal("800000.00"),
        equity=Decimal("1500000.00"),
        ebitda=Decimal("900000.00"),
        source="AUDITED"
    )


@pytest.mark.django_db
def test_create_company(api_client):
    """Test creating a company via API"""
    url = reverse('company-list')
    data = {
        'name': 'New Company Pty Ltd',
        'trading_name': 'New Company',
        'company_type': 'PTY_LTD',
        'acn': '987654321',
        'abn': '98765432109',
        'registration_date': '2015-01-01',
        'registration_jurisdiction': 'VIC',
        'registered_address_line1': '123 New St',
        'registered_city': 'Melbourne',
        'registered_state': 'VIC',
        'registered_postal_code': '3000',
        'registered_country': 'Australia',
        'business_address_line1': '123 New St',
        'business_city': 'Melbourne',
        'business_state': 'VIC',
        'business_postal_code': '3000',
        'business_country': 'Australia',
        'phone': '0387654321',
        'email': 'info@newcompany.com.au',
        'website': 'https://www.newcompany.com.au',
        'industry': 'Finance',
        'business_description': 'Financial services',
        'employees_count': 10,
        'years_in_business': 8
    }
    
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Company.objects.count() == 1
    assert Company.objects.get().name == 'New Company Pty Ltd'


@pytest.mark.django_db
def test_get_company_list(api_client, sample_company):
    """Test getting a list of companies"""
    url = reverse('company-list')
    response = api_client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'Test Company Pty Ltd'
    assert 'directors_count' in response.data[0]
    assert 'shareholders_count' in response.data[0]


@pytest.mark.django_db
def test_get_company_detail(api_client, sample_company, sample_director, sample_shareholder, sample_financial):
    """Test getting company details"""
    url = reverse('company-detail', kwargs={'pk': sample_company.pk})
    response = api_client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == 'Test Company Pty Ltd'
    assert 'registered_address' in response.data
    assert 'business_address' in response.data
    assert 'directors' in response.data
    assert 'shareholders' in response.data
    assert 'latest_financial' in response.data
    assert 'financials' in response.data
    assert len(response.data['directors']) == 1
    assert len(response.data['shareholders']) == 1
    assert len(response.data['financials']) == 1


@pytest.mark.django_db
def test_update_company(api_client, sample_company):
    """Test updating a company"""
    url = reverse('company-detail', kwargs={'pk': sample_company.pk})
    data = {
        'name': 'Updated Company Pty Ltd',
        'employees_count': 30
    }
    
    response = api_client.patch(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    
    sample_company.refresh_from_db()
    assert sample_company.name == 'Updated Company Pty Ltd'
    assert sample_company.employees_count == 30


@pytest.mark.django_db
def test_delete_company(api_client, sample_company):
    """Test deleting a company"""
    url = reverse('company-detail', kwargs={'pk': sample_company.pk})
    response = api_client.delete(url)
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Company.objects.count() == 0


@pytest.mark.django_db
def test_create_director(api_client, sample_company):
    """Test creating a director via API"""
    url = reverse('director-list')
    data = {
        'company': str(sample_company.id),
        'first_name': 'Jane',
        'last_name': 'Doe',
        'date_of_birth': '1980-03-15',
        'appointment_date': '2015-01-01',
        'role': 'EXECUTIVE_DIRECTOR',
        'residential_address_line1': '123 Director St',
        'residential_city': 'Sydney',
        'residential_state': 'NSW',
        'residential_postal_code': '2000',
        'residential_country': 'Australia',
        'phone': '0423456789',
        'email': 'jane.doe@testcompany.com.au',
        'identification_type': 'PASSPORT',
        'identification_number': 'PA123456'
    }
    
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Director.objects.count() == 1
    assert Director.objects.get().first_name == 'Jane'


@pytest.mark.django_db
def test_create_shareholder(api_client, sample_company, sample_director):
    """Test creating a shareholder via API"""
    url = reverse('shareholder-list')
    data = {
        'company': str(sample_company.id),
        'shareholder_type': 'INDIVIDUAL',
        'individual_first_name': 'Jane',
        'individual_last_name': 'Doe',
        'individual_date_of_birth': '1980-03-15',
        'shareholding_percentage': 40.0,
        'share_class': 'ORDINARY',
        'acquisition_date': '2015-01-01',
        'is_director': False
    }
    
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Shareholder.objects.count() == 1
    assert Shareholder.objects.get().individual_first_name == 'Jane'


@pytest.mark.django_db
def test_create_financial_information(api_client, sample_company):
    """Test creating financial information via API"""
    url = reverse('financialinformation-list')
    data = {
        'company': str(sample_company.id),
        'financial_year': '2023',
        'financial_year_end_date': '2023-06-30',
        'annual_revenue': '6000000.00',
        'annual_profit': '900000.00',
        'total_assets': '3500000.00',
        'total_liabilities': '1800000.00',
        'current_assets': '1500000.00',
        'current_liabilities': '900000.00',
        'equity': '1700000.00',
        'ebitda': '1100000.00',
        'source': 'AUDITED'
    }
    
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert FinancialInformation.objects.count() == 1
    assert FinancialInformation.objects.get().financial_year == '2023'


@pytest.mark.django_db
def test_company_directors_endpoint(api_client, sample_company, sample_director):
    """Test company directors endpoint"""
    url = reverse('company-directors', kwargs={'pk': sample_company.pk})
    response = api_client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['full_name'] == 'John Smith'


@pytest.mark.django_db
def test_company_shareholders_endpoint(api_client, sample_company, sample_shareholder):
    """Test company shareholders endpoint"""
    url = reverse('company-shareholders', kwargs={'pk': sample_company.pk})
    response = api_client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['shareholder_name'] == 'John Smith'
    assert response.data[0]['shareholding_percentage'] == '60.00'


@pytest.mark.django_db
def test_company_financials_endpoint(api_client, sample_company, sample_financial):
    """Test company financials endpoint"""
    url = reverse('company-financials', kwargs={'pk': sample_company.pk})
    response = api_client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['financial_year'] == '2022'
    assert response.data[0]['annual_revenue'] == '5000000.00'


@pytest.mark.django_db
def test_company_latest_financial_endpoint(api_client, sample_company, sample_financial):
    """Test company latest financial endpoint"""
    url = reverse('company-latest-financial', kwargs={'pk': sample_company.pk})
    response = api_client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data['financial_year'] == '2022'
    assert response.data['annual_revenue'] == '5000000.00'
    assert 'current_ratio' in response.data
    assert 'debt_to_equity_ratio' in response.data
    assert 'profit_margin' in response.data
