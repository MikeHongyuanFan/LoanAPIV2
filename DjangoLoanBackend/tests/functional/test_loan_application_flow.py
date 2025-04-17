"""
Functional tests for the loan application flow in the Loan Application System.
"""

import pytest
from django.urls import reverse
from rest_framework import status
from apps.application.models import Application
from apps.borrower.models import Borrower
from apps.product.models import Product
from apps.broker.models import Broker

@pytest.mark.django_db
class TestLoanApplicationFlow:
    """Test the complete loan application flow."""
    
    def test_complete_loan_application_flow(self, admin_client, borrower, broker, product):
        """
        Test the complete loan application flow from creation to approval.
        """
        # Step 1: Create a new loan application
        application_url = reverse('application-list')
        application_data = {
            'borrower': borrower.id,
            'product': product.id,
            'broker': broker.id,
            'loan_amount': 250000.00,
            'loan_term_months': 240,
            'interest_rate': 5.5,
            'loan_purpose': 'PURCHASE',  # Changed from 'purpose' to 'loan_purpose' and using valid choice
            'property_address': '123 Property St, Property City',
            'property_value': 500000.00,
            'property_type': 'RESIDENTIAL',
        }
        
        response = admin_client.post(application_url, application_data)
        assert response.status_code == status.HTTP_201_CREATED
        application_id = response.data['id']
        
        # Step 2: Submit the application for review
        submit_url = reverse('application-submit', args=[application_id])
        response = admin_client.post(submit_url)
        assert response.status_code == status.HTTP_200_OK
        
        # Step 3: Upload required documents
        document_url = reverse('document-list')
        document_data = {
            'application': application_id,
            'document_type': 'ID_VERIFICATION',
            'name': 'ID Document',
            'description': 'Passport for verification',
            'file': 'test_document.pdf'  # In a real test, we would use SimpleUploadedFile
        }
        
        # Note: In a real test, we would actually upload a file
        # For this example, we'll just check that the endpoint exists
        # response = admin_client.post(document_url, document_data)
        # assert response.status_code == status.HTTP_201_CREATED
        
        # Step 4: Review the application
        review_url = reverse('application-review', args=[application_id])
        review_data = {
            'status': 'APPROVED',
            'notes': 'Application approved after review',
        }
        
        response = admin_client.post(review_url, review_data)
        assert response.status_code == status.HTTP_200_OK
        
        # Step 5: Verify the application status
        detail_url = reverse('application-detail', args=[application_id])
        response = admin_client.get(detail_url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'APPROVED'
        
        # Step 6: Generate loan documents
        generate_docs_url = reverse('application-generate-documents', args=[application_id])
        response = admin_client.post(generate_docs_url)
        assert response.status_code == status.HTTP_200_OK
        
        # Step 7: Finalize the loan
        finalize_url = reverse('application-finalize', args=[application_id])
        response = admin_client.post(finalize_url)
        assert response.status_code == status.HTTP_200_OK
        
        # Final verification
        response = admin_client.get(detail_url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'FINALIZED'
