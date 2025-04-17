"""
Unit tests for models in the Loan Application System.
"""

import pytest
from django.test import TestCase
from apps.borrower.models import Borrower
from apps.broker.models import Broker
from apps.product.models import Product
from apps.application.models import Application

class TestBorrowerModel(TestCase):
    """Test cases for the Borrower model."""
    
    def setUp(self):
        self.borrower = Borrower.objects.create(
            name='Test Borrower',
            email='test@example.com',
            phone='1234567890',
            address='123 Test St, Test City',
            date_of_birth='1980-01-01',
            gender='M',
            id_number='ID12345',
            id_type='Passport',
            employment_status='EMPLOYED',
            employer='Test Company',
            income=50000.00
        )
    
    def test_borrower_creation(self):
        """Test that a borrower can be created."""
        self.assertEqual(self.borrower.name, 'Test Borrower')
        self.assertEqual(self.borrower.email, 'test@example.com')
        self.assertEqual(self.borrower.income, 50000.00)
    
    def test_borrower_str(self):
        """Test the string representation of a borrower."""
        self.assertEqual(str(self.borrower), 'Test Borrower')


class TestBrokerModel(TestCase):
    """Test cases for the Broker model."""
    
    def setUp(self):
        self.broker = Broker.objects.create(
            name='Test Broker',
            email='broker@example.com',
            phone='0987654321',
            company='Test Brokerage',
            address='456 Broker St, Broker City',
            license_number='BRK12345',
            commission_rate=2.5
        )
    
    def test_broker_creation(self):
        """Test that a broker can be created."""
        self.assertEqual(self.broker.name, 'Test Broker')
        self.assertEqual(self.broker.company, 'Test Brokerage')
        self.assertEqual(self.broker.commission_rate, 2.5)
    
    def test_broker_str(self):
        """Test the string representation of a broker."""
        self.assertEqual(str(self.broker), 'Test Broker (Test Brokerage)')


class TestProductModel(TestCase):
    """Test cases for the Product model."""
    
    def setUp(self):
        self.product = Product.objects.create(
            name='Test Loan Product',
            description='A test loan product for testing',
            loan_type='MORTGAGE',
            min_loan_amount=10000.00,
            max_loan_amount=500000.00,
            min_interest_rate=3.5,
            max_interest_rate=7.5,
            min_term_months=12,
            max_term_months=360,
            establishment_fee=1000.00
        )
    
    def test_product_creation(self):
        """Test that a product can be created."""
        self.assertEqual(self.product.name, 'Test Loan Product')
        self.assertEqual(self.product.loan_type, 'MORTGAGE')
        self.assertEqual(self.product.min_loan_amount, 10000.00)
    
    def test_product_str(self):
        """Test the string representation of a product."""
        self.assertEqual(str(self.product), 'Test Loan Product (MORTGAGE)')
