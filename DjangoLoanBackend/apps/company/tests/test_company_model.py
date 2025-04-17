import pytest
from django.core.exceptions import ValidationError
from apps.company.models import Company, Director, Shareholder, FinancialInformation
import datetime
from decimal import Decimal


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
def test_company_creation(sample_company):
    """Test creating a company"""
    assert Company.objects.count() == 1
    assert str(sample_company) == "Test Company Pty Ltd"
    assert sample_company.get_registered_address()['city'] == "Sydney"
    assert sample_company.get_business_address()['line1'] == "456 Business St"


@pytest.mark.django_db
def test_director_creation(sample_director):
    """Test creating a director"""
    assert Director.objects.count() == 1
    assert sample_director.get_full_name() == "John Smith"
    assert sample_director.get_residential_address()['city'] == "Sydney"
    assert not sample_director.is_shareholder()


@pytest.mark.django_db
def test_shareholder_creation(sample_shareholder):
    """Test creating a shareholder"""
    assert Shareholder.objects.count() == 1
    assert sample_shareholder.get_shareholder_name() == "John Smith"
    assert sample_shareholder.is_director
    assert sample_shareholder.director is not None


@pytest.mark.django_db
def test_financial_information_creation(sample_financial):
    """Test creating financial information"""
    assert FinancialInformation.objects.count() == 1
    assert sample_financial.get_current_ratio() == Decimal("1.5")
    assert sample_financial.get_debt_to_equity_ratio() == Decimal("1.0")
    assert sample_financial.get_profit_margin() == Decimal("0.15")


@pytest.mark.django_db
def test_company_relationships(sample_company, sample_director, sample_shareholder, sample_financial):
    """Test company relationships"""
    assert sample_company.get_directors_count() == 1
    assert sample_company.get_shareholders_count() == 1
    assert sample_company.get_latest_financial_year() == sample_financial


@pytest.mark.django_db
def test_director_shareholder_relationship(sample_director, sample_shareholder):
    """Test director-shareholder relationship"""
    # After creating the shareholder linked to the director
    assert sample_director.is_shareholder()
    assert sample_director.shareholdings.count() == 1
    assert sample_director.shareholdings.first() == sample_shareholder


@pytest.mark.django_db
def test_shareholder_validation():
    """Test shareholder validation"""
    company = Company.objects.create(
        name="Test Company 2 Pty Ltd",
        company_type="PTY_LTD",
        registration_date=datetime.date(2010, 1, 1),
        registration_jurisdiction="NSW",
        registered_address_line1="123 Test St",
        registered_city="Sydney",
        registered_state="NSW",
        registered_postal_code="2000",
        business_address_line1="123 Test St",
        business_city="Sydney",
        business_state="NSW",
        business_postal_code="2000",
        phone="0298765432",
        email="info@test2.com.au",
        industry="Technology",
        business_description="Testing"
    )
    
    # Create a corporate shareholder
    corporate_shareholder = Shareholder(
        company=company,
        shareholder_type="CORPORATE",
        corporate_name="Corporate Investor Ltd",
        shareholding_percentage=Decimal("40.0"),
        share_class="ORDINARY",
        acquisition_date=datetime.date(2010, 1, 1)
    )
    corporate_shareholder.full_clean()  # Should not raise ValidationError
    corporate_shareholder.save()
    
    # Create an invalid shareholder (corporate but marked as director)
    with pytest.raises(ValidationError):
        invalid_shareholder = Shareholder(
            company=company,
            shareholder_type="CORPORATE",
            corporate_name="Invalid Corp",
            shareholding_percentage=Decimal("20.0"),
            share_class="ORDINARY",
            acquisition_date=datetime.date(2010, 1, 1),
            is_director=True  # This should cause validation error without director
        )
        invalid_shareholder.full_clean()


@pytest.mark.django_db
def test_financial_calculations(sample_financial):
    """Test financial calculations"""
    # Test current ratio
    assert sample_financial.get_current_ratio() == Decimal("1.5")  # 1200000 / 800000
    
    # Test debt-to-equity ratio
    assert sample_financial.get_debt_to_equity_ratio() == Decimal("1.0")  # 1500000 / 1500000
    
    # Test profit margin
    assert sample_financial.get_profit_margin() == Decimal("0.15")  # 750000 / 5000000
    
    # Test with zero values
    zero_financial = FinancialInformation.objects.create(
        company=sample_financial.company,
        financial_year="2021",
        financial_year_end_date=datetime.date(2021, 6, 30),
        annual_revenue=Decimal("0.00"),
        annual_profit=Decimal("0.00"),
        total_assets=Decimal("1000000.00"),
        total_liabilities=Decimal("500000.00"),
        current_assets=Decimal("0.00"),
        current_liabilities=Decimal("0.00"),
        equity=Decimal("0.00"),
        ebitda=Decimal("0.00"),
        source="MANAGEMENT"
    )
    
    assert zero_financial.get_current_ratio() is None  # Division by zero
    assert zero_financial.get_debt_to_equity_ratio() is None  # Division by zero
    assert zero_financial.get_profit_margin() is None  # Division by zero
