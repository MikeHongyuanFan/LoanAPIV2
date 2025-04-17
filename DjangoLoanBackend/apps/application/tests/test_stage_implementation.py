import pytest
from django.utils import timezone
from datetime import timedelta
from unittest.mock import patch
from apps.application.models import Application
from apps.notification.models import Notification
from apps.borrower.models import Borrower
from apps.broker.models import Broker
from apps.product.models import Product
from django.core import mail
from django.test import override_settings


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
def test_application_stage_field(sample_application):
    """Test that the stage field is added to the Application model"""
    assert hasattr(sample_application, 'stage')
    assert sample_application.stage == "ENQUIRY"
    
    # Test stage choices
    sample_application.stage = "INDICATIVE_OFFER"
    sample_application.save()
    assert sample_application.stage == "INDICATIVE_OFFER"


@pytest.mark.django_db
def test_stage_changed_at_field(sample_application):
    """Test that the stage_changed_at field is updated when stage changes"""
    original_changed_at = sample_application.stage_changed_at
    
    # Wait a moment to ensure timestamp difference
    import time
    time.sleep(1)
    
    # Change stage
    sample_application.stage = "INDICATIVE_OFFER"
    sample_application.save()
    
    # Refresh from database
    sample_application.refresh_from_db()
    
    # Check that stage_changed_at was updated
    assert sample_application.stage_changed_at > original_changed_at


@pytest.mark.django_db
def test_valuer_qs_info_fields(sample_application):
    """Test that the valuer_info and qs_info fields are added to the Application model"""
    assert hasattr(sample_application, 'valuer_info')
    assert hasattr(sample_application, 'qs_info')
    
    # Test setting and retrieving JSON data
    valuer_data = {
        "company_name": "Test Valuer Company",
        "contact_name": "John Valuer",
        "email": "valuer@example.com",
        "phone": "1122334455"
    }
    
    qs_data = {
        "company_name": "Test QS Company",
        "contact_name": "Jane QS",
        "email": "qs@example.com",
        "phone": "5544332211"
    }
    
    sample_application.valuer_info = valuer_data
    sample_application.qs_info = qs_data
    sample_application.save()
    
    # Refresh from database
    sample_application.refresh_from_db()
    
    # Check that data was saved correctly
    assert sample_application.valuer_info == valuer_data
    assert sample_application.qs_info == qs_data


@pytest.mark.django_db
@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
def test_stage_change_notification(sample_application):
    """Test that notifications are created when stage changes"""
    # Clear existing notifications
    Notification.objects.all().delete()
    
    # Change stage
    sample_application.stage = "INDICATIVE_OFFER"
    sample_application.save()
    
    # Check that notification was created
    notifications = Notification.objects.filter(
        type='STAGE_CHANGE',
        related_id=sample_application.id
    )
    assert notifications.count() == 1
    assert "changed to" in notifications.first().subject
    assert "INDICATIVE_OFFER" in notifications.first().message


@pytest.mark.django_db
@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
def test_stage_change_email(sample_application):
    """Test that emails are sent when stage changes"""
    # Change stage
    sample_application.stage = "INDICATIVE_OFFER"
    sample_application.save()
    
    # Check that emails were sent
    assert len(mail.outbox) == 2  # One for broker, one for borrower
    
    # Check broker email
    broker_email = None
    borrower_email = None
    for email in mail.outbox:
        if sample_application.broker.email in email.to:
            broker_email = email
        if sample_application.borrower.email in email.to:
            borrower_email = email
    
    assert broker_email is not None
    assert "Stage Update" in broker_email.subject
    assert sample_application.reference_number in broker_email.subject
    assert "Indicative Offer" in broker_email.body
    
    # Check borrower email
    assert borrower_email is not None
    assert "Update" in borrower_email.subject
    assert sample_application.reference_number in borrower_email.subject
    assert "Indicative Offer" in borrower_email.body


@pytest.mark.django_db
def test_stagnation_check_command():
    """Test the stagnation check command"""
    from django.core.management import call_command
    from io import StringIO
    
    # Create an application with an old stage_changed_at
    borrower = Borrower.objects.create(
        name="Test Borrower",
        email="borrower@example.com",
        phone="1234567890",
        address="123 Test St"
    )
    
    broker = Broker.objects.create(
        name="Test Broker",
        company="Test Company",
        email="broker@example.com",
        phone="0987654321"
    )
    
    product = Product.objects.create(
        name="Test Product",
        description="Test Description",
        interest_rate=5.0
    )
    
    app = Application.objects.create(
        borrower=borrower,
        broker=broker,
        product=product,
        loan_amount=100000,
        loan_term_months=12,
        interest_rate=5.0,
        loan_purpose="PURCHASE",
        property_address="123 Test St",
        property_type="HOUSE",
        property_value=150000,
        stage="ENQUIRY"
    )
    
    # Set stage_changed_at to 4 days ago (threshold for ENQUIRY is 3 days)
    app.stage_changed_at = timezone.now() - timedelta(days=4)
    app.save(update_fields=['stage_changed_at'])
    
    # Clear existing notifications
    Notification.objects.all().delete()
    
    # Call the command
    out = StringIO()
    call_command('check_stagnant_applications', stdout=out)
    
    # Check output
    output = out.getvalue()
    assert app.reference_number in output
    assert "has been in ENQUIRY stage" in output
    
    # Check that notification was created
    notifications = Notification.objects.filter(
        type='STAGE_STAGNATION',
        related_id=app.id
    )
    assert notifications.count() == 1
    assert "stagnant" in notifications.first().subject
    assert app.reference_number in notifications.first().message
