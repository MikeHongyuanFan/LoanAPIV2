import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestBorrowerWorkflow:
    """
    Functional tests for borrower-related workflows.
    """
    
    def test_create_borrower_workflow(self, staff_client):
        """
        Test the complete workflow for creating a borrower.
        """
        # Step 1: Create a borrower
        create_url = reverse('borrower-list')
        borrower_data = {
            'name': 'Alice Johnson',
            'email': 'alice@example.com',
            'phone': '1234567890',
            'address': '123 Test St, Test City',
            'date_of_birth': '1985-05-15',
            'gender': 'F',
            'id_number': 'ID123456',
            'id_type': 'Passport',
            'employment_status': 'EMPLOYED',
            'employer': 'Test Company',
            'income': 75000.00
        }
        
        response = staff_client.post(create_url, borrower_data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        borrower_id = response.data['id']
        
        # Step 2: Verify the borrower was created correctly
        detail_url = reverse('borrower-detail', kwargs={'pk': borrower_id})
        response = staff_client.get(detail_url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Alice Johnson'
        assert response.data['email'] == 'alice@example.com'
        
        # Step 3: Check for potential duplicates
        check_duplicates_url = reverse('borrower-check-duplicates')
        duplicate_check_data = {
            'name': 'Alice Johnson',
            'email': 'different@example.com',
            'phone': '0987654321',
            'id_number': 'ID654321'
        }
        
        response = staff_client.post(check_duplicates_url, duplicate_check_data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0  # Should find at least one potential duplicate
        
        # Step 4: Update the borrower
        update_data = {
            'employer': 'New Company',
            'income': 85000.00
        }
        
        response = staff_client.patch(detail_url, update_data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['employer'] == 'New Company'
        assert response.data['income'] == '85000.00'
        
        # Step 5: Get all borrowers and verify the updated one is there
        list_url = reverse('borrower-list')
        response = staff_client.get(list_url)
        
        assert response.status_code == status.HTTP_200_OK
        assert any(b['name'] == 'Alice Johnson' and b['employer'] == 'New Company' for b in response.data['results'])
    
    def test_merge_borrowers_workflow(self, staff_client):
        """
        Test the workflow for merging duplicate borrowers.
        """
        # Step 1: Create first borrower
        create_url = reverse('borrower-list')
        borrower1_data = {
            'name': 'Bob Smith',
            'email': 'bob@example.com',
            'phone': '1234567890',
            'address': '123 Test St, Test City',
            'date_of_birth': '1980-10-20',
            'gender': 'M',
            'id_number': 'ID123456',
            'id_type': 'Passport',
            'employment_status': 'EMPLOYED',
            'employer': 'Test Company',
            'income': 65000.00
        }
        
        response = staff_client.post(create_url, borrower1_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        borrower1_id = response.data['id']
        
        # Step 2: Create second borrower (potential duplicate)
        borrower2_data = {
            'name': 'Robert Smith',  # Similar name
            'email': 'robert@example.com',
            'phone': '0987654321',
            'address': '456 Other St, Other City',
            'date_of_birth': '1980-10-20',  # Same DOB
            'gender': 'M',
            'id_number': 'ID654321',
            'id_type': 'Driver License',
            'employment_status': 'SELF_EMPLOYED',
            'employer': None,
            'income': 70000.00
        }
        
        response = staff_client.post(create_url, borrower2_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        borrower2_id = response.data['id']
        
        # Step 3: Check for duplicates
        check_duplicates_url = reverse('borrower-check-duplicates')
        duplicate_check_data = {
            'name': 'Bob Smith',
            'date_of_birth': '1980-10-20'
        }
        
        response = staff_client.post(check_duplicates_url, duplicate_check_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0
        
        # Step 4: Merge the borrowers
        merge_url = reverse('borrower-merge')
        merge_data = {
            'primary_borrower_id': borrower1_id,
            'duplicate_borrower_id': borrower2_id,
            'fields_to_keep': {
                'phone': 'duplicate',  # Keep phone from duplicate
                'income': 'duplicate',  # Keep income from duplicate
                'id_type': 'duplicate'  # Keep ID type from duplicate
            }
        }
        
        response = staff_client.post(merge_url, merge_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        
        # Step 5: Verify the merged borrower has the correct information
        detail_url = reverse('borrower-detail', kwargs={'pk': borrower1_id})
        response = staff_client.get(detail_url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Bob Smith'  # Original name
        assert response.data['phone'] == '0987654321'  # From duplicate
        assert response.data['income'] == '70000.00'  # From duplicate
        assert response.data['id_type'] == 'Driver License'  # From duplicate
        
        # Step 6: Verify the duplicate borrower no longer exists
        detail_url = reverse('borrower-detail', kwargs={'pk': borrower2_id})
        response = staff_client.get(detail_url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
        # Step 7: Check merge history
        merge_history_url = reverse('borrower-merge-history')
        response = staff_client.get(merge_history_url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0
        assert any(m['primary_borrower_id'] == borrower1_id for m in response.data['results'])
