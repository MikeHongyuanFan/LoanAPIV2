import pytest
from apps.borrower.models import Borrower


@pytest.mark.django_db
class TestBorrowerModel:
    """
    Test cases for the Borrower model.
    """
    
    def test_create_borrower(self):
        """
        Test creating a borrower.
        """
        borrower = Borrower.objects.create(
            name='John Doe',
            email='john@example.com',
            phone='1234567890',
            address='123 Main St, City',
            date_of_birth='1985-05-15',
            gender='M',
            id_number='ID123456',
            id_type='Driver License',
            employment_status='EMPLOYED',
            employer='ABC Company',
            income=75000.00
        )
        
        assert borrower.id is not None
        assert borrower.name == 'John Doe'
        assert borrower.email == 'john@example.com'
        assert borrower.phone == '1234567890'
        assert borrower.address == '123 Main St, City'
        assert str(borrower.date_of_birth) == '1985-05-15'
        assert borrower.gender == 'M'
        assert borrower.id_number == 'ID123456'
        assert borrower.id_type == 'Driver License'
        assert borrower.employment_status == 'EMPLOYED'
        assert borrower.employer == 'ABC Company'
        assert borrower.income == 75000.00
    
    def test_borrower_str_method(self):
        """
        Test the string representation of a borrower.
        """
        borrower = Borrower.objects.create(
            name='Jane Smith',
            email='jane@example.com',
            phone='0987654321',
            address='456 Oak St, Town',
            date_of_birth='1990-10-20',
            gender='F',
            id_number='ID654321',
            id_type='Passport',
            employment_status='SELF_EMPLOYED',
            employer=None,
            income=60000.00
        )
        
        assert str(borrower) == 'Jane Smith'
    
    def test_find_potential_duplicates_by_name(self):
        """
        Test finding potential duplicates by name.
        """
        # Create original borrower
        Borrower.objects.create(
            name='Michael Johnson',
            email='michael@example.com',
            phone='1122334455',
            address='789 Pine St, Village',
            date_of_birth='1975-03-10',
            gender='M',
            id_number='ID112233',
            id_type='Passport',
            employment_status='EMPLOYED',
            employer='XYZ Corp',
            income=90000.00
        )
        
        # Create a borrower with the same name but different details
        Borrower.objects.create(
            name='Michael Johnson',
            email='different@example.com',
            phone='5566778899',
            address='101 Elm St, County',
            date_of_birth='1980-07-22',
            gender='M',
            id_number='ID445566',
            id_type='Driver License',
            employment_status='SELF_EMPLOYED',
            employer=None,
            income=70000.00
        )
        
        # Search for duplicates
        duplicates = Borrower.find_potential_duplicates({
            'name': 'Michael Johnson',
            'email': 'new@example.com',
            'phone': '9988776655',
            'id_number': 'ID778899'
        })
        
        assert duplicates.count() == 2
    
    def test_find_potential_duplicates_by_email(self):
        """
        Test finding potential duplicates by email.
        """
        # Create original borrower
        Borrower.objects.create(
            name='Robert Brown',
            email='robert@example.com',
            phone='2233445566',
            address='202 Cedar St, District',
            date_of_birth='1982-11-05',
            gender='M',
            id_number='ID223344',
            id_type='Passport',
            employment_status='EMPLOYED',
            employer='LMN Inc',
            income=85000.00
        )
        
        # Search for duplicates
        duplicates = Borrower.find_potential_duplicates({
            'name': 'Bob Brown',
            'email': 'robert@example.com',
            'phone': '6677889900',
            'id_number': 'ID667788'
        })
        
        assert duplicates.count() == 1
        assert duplicates.first().name == 'Robert Brown'
    
    def test_find_potential_duplicates_by_phone(self):
        """
        Test finding potential duplicates by phone.
        """
        # Create original borrower
        Borrower.objects.create(
            name='Sarah Wilson',
            email='sarah@example.com',
            phone='3344556677',
            address='303 Birch St, Borough',
            date_of_birth='1988-09-15',
            gender='F',
            id_number='ID334455',
            id_type='Driver License',
            employment_status='EMPLOYED',
            employer='PQR Ltd',
            income=65000.00
        )
        
        # Search for duplicates
        duplicates = Borrower.find_potential_duplicates({
            'name': 'Sara Wilson',
            'email': 'different@example.com',
            'phone': '3344556677',
            'id_number': 'ID998877'
        })
        
        assert duplicates.count() == 1
        assert duplicates.first().name == 'Sarah Wilson'
    
    def test_find_potential_duplicates_by_id_number(self):
        """
        Test finding potential duplicates by ID number.
        """
        # Create original borrower
        Borrower.objects.create(
            name='David Miller',
            email='david@example.com',
            phone='4455667788',
            address='404 Maple St, Township',
            date_of_birth='1979-12-25',
            gender='M',
            id_number='ID445566',
            id_type='Passport',
            employment_status='RETIRED',
            employer=None,
            income=45000.00
        )
        
        # Search for duplicates
        duplicates = Borrower.find_potential_duplicates({
            'name': 'Dave Miller',
            'email': 'dave@example.com',
            'phone': '8877665544',
            'id_number': 'ID445566'
        })
        
        assert duplicates.count() == 1
        assert duplicates.first().name == 'David Miller'
    
    def test_find_potential_duplicates_with_model_instance(self):
        """
        Test finding potential duplicates using a model instance.
        """
        # Create original borrower
        Borrower.objects.create(
            name='Emily Davis',
            email='emily@example.com',
            phone='5566778899',
            address='505 Walnut St, Hamlet',
            date_of_birth='1992-04-30',
            gender='F',
            id_number='ID556677',
            id_type='Driver License',
            employment_status='EMPLOYED',
            employer='STU Corp',
            income=72000.00
        )
        
        # Create a new borrower instance (not saved)
        new_borrower = Borrower(
            name='Emily Davis',
            email='different@example.com',
            phone='9988776655',
            address='606 Pineapple St, Village',
            date_of_birth='1992-04-30',
            gender='F',
            id_number='ID667788',
            id_type='Passport',
            employment_status='SELF_EMPLOYED',
            employer=None,
            income=68000.00
        )
        
        # Search for duplicates
        duplicates = Borrower.find_potential_duplicates(new_borrower)
        
        assert duplicates.count() == 1
        assert duplicates.first().name == 'Emily Davis'
