import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.borrower.models import Borrower
from apps.broker.models import Broker
from apps.product.models import Product
from apps.application.models import Application
from django.utils import timezone
from decimal import Decimal

User = get_user_model()

@pytest.fixture
def api_client():
    """
    Return a DRF API client for testing API endpoints.
    """
    return APIClient()

@pytest.fixture
def regular_user(django_user_model):
    """
    Create and return a regular (non-staff) user.
    """
    return django_user_model.objects.create_user(
        username='regular_user',
        email='regular@example.com',
        password='password123',
        is_staff=False
    )

@pytest.fixture
def staff_user(django_user_model):
    """
    Create and return a staff user.
    """
    return django_user_model.objects.create_user(
        username='staff_user',
        email='staff@example.com',
        password='password123',
        is_staff=True
    )

@pytest.fixture
def authenticated_client(regular_user):
    """
    Return an authenticated API client for a regular user.
    """
    client = APIClient()
    client.force_authenticate(user=regular_user)
    return client

@pytest.fixture
def staff_client(staff_user):
    """
    Return an authenticated API client for a staff user.
    """
    client = APIClient()
    client.force_authenticate(user=staff_user)
    return client

@pytest.fixture
def borrower():
    """
    Create and return a test borrower.
    """
    return Borrower.objects.create(
        name="Test Borrower",
        email="test@borrower.com",
        phone="1234567890",
        address="123 Borrower St, Test City",
        date_of_birth=timezone.now().date() - timezone.timedelta(days=365*30),
        gender="M",
        id_number="ID12345678",
        id_type="PASSPORT",
        employment_status="EMPLOYED",
        employer="Test Company",
        income=Decimal("75000.00")
    )

@pytest.fixture
def broker():
    """
    Create and return a test broker.
    """
    return Broker.objects.create(
        name="Test Broker",
        email="test@broker.com",
        phone="5555555555",
        company="Test Brokerage",
        address="123 Broker St, Test City",
        license_number="BRK12345",
        commission_rate=Decimal("2.0")
    )

@pytest.fixture
def product():
    """
    Create and return a test loan product.
    """
    return Product.objects.create(
        name="Test Loan Product",
        description="A test loan product for testing",
        loan_type="MORTGAGE",
        min_loan_amount=Decimal("50000.00"),
        max_loan_amount=Decimal("1000000.00"),
        min_term_months=12,
        max_term_months=360,
        min_interest_rate=Decimal("3.5"),
        max_interest_rate=Decimal("7.5"),
        establishment_fee=Decimal("1000.00"),
        active=True
    )

@pytest.fixture
def application(borrower, broker, product):
    """
    Create and return a test loan application.
    """
    return Application.objects.create(
        borrower=borrower,
        broker=broker,
        product=product,
        loan_amount=Decimal("250000.00"),
        loan_term_months=240,
        interest_rate=Decimal("5.5"),
        loan_purpose="PURCHASE",
        property_address="123 Property St, Property City",
        property_value=Decimal("500000.00"),
        property_type="RESIDENTIAL",
        status="DRAFT"
    )
