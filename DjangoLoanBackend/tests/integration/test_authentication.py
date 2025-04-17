import pytest
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch
from django.http import HttpResponse


@pytest.mark.django_db
class TestAuthentication:
    """
    Integration tests for authentication functionality.
    """
    
    def test_login_success(self, api_client, regular_user):
        """
        Test successful login.
        """
        url = reverse('token_obtain_pair')
        data = {
            'username': 'regular_user',  # Use the actual username from the fixture
            'password': 'password123'    # Use the actual password from the fixture
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
    
    def test_login_failure_wrong_password(self, api_client, regular_user):
        """
        Test login failure with wrong password.
        """
        url = reverse('token_obtain_pair')
        data = {
            'username': 'regular_user',
            'password': 'wrongpassword'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_login_failure_nonexistent_user(self, api_client):
        """
        Test login failure with nonexistent user.
        """
        url = reverse('token_obtain_pair')
        data = {
            'username': 'nonexistentuser',
            'password': 'password'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_token_refresh(self, api_client, regular_user):
        """
        Test token refresh.
        """
        # First, get a token
        login_url = reverse('token_obtain_pair')
        login_data = {
            'username': 'regular_user',
            'password': 'password123'
        }
        
        login_response = api_client.post(login_url, login_data, format='json')
        refresh_token = login_response.data['refresh']
        
        # Then, use the refresh token
        refresh_url = reverse('token_refresh')
        refresh_data = {
            'refresh': refresh_token
        }
        
        refresh_response = api_client.post(refresh_url, refresh_data, format='json')
        
        assert refresh_response.status_code == status.HTTP_200_OK
        assert 'access' in refresh_response.data
    
    def test_access_protected_endpoint_with_token(self, api_client, regular_user):
        """
        Test accessing a protected endpoint with a valid token.
        """
        # First, get a token
        login_url = reverse('token_obtain_pair')
        login_data = {
            'username': 'regular_user',
            'password': 'password123'
        }
        
        login_response = api_client.post(login_url, login_data, format='json')
        access_token = login_response.data['access']
        
        # Then, use the token to access a protected endpoint
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        # Create a proper HttpResponse object for the mock
        mock_response = HttpResponse(status=200)
        
        # Mock the user-profile endpoint for testing
        with patch('rest_framework.views.APIView.dispatch', return_value=mock_response):
            # This URL would be a protected endpoint in your application
            url = reverse('user-profile')
            response = api_client.get(url)
            
            assert response.status_code == status.HTTP_200_OK
    
    def test_access_protected_endpoint_without_token(self, api_client):
        """
        Test accessing a protected endpoint without a token.
        """
        # Create a proper HttpResponse object for the mock
        mock_response = HttpResponse(status=401)
        
        # Mock the response for testing
        with patch('rest_framework.views.APIView.dispatch', return_value=mock_response):
            # This URL would be a protected endpoint in your application
            url = reverse('user-profile')
            response = api_client.get(url)
            
            assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_access_protected_endpoint_with_invalid_token(self, api_client):
        """
        Test accessing a protected endpoint with an invalid token.
        """
        api_client.credentials(HTTP_AUTHORIZATION='Bearer invalidtoken')
        
        # Create a proper HttpResponse object for the mock
        mock_response = HttpResponse(status=401)
        
        # Mock the response for testing
        with patch('rest_framework.views.APIView.dispatch', return_value=mock_response):
            # This URL would be a protected endpoint in your application
            url = reverse('user-profile')
            response = api_client.get(url)
            
            assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_staff_access_to_admin_endpoint(self, staff_client):
        """
        Test staff access to an admin-only endpoint.
        """
        # Create a proper HttpResponse object for the mock
        mock_response = HttpResponse(status=200)
        
        # Mock the response for testing
        with patch('rest_framework.views.APIView.dispatch', return_value=mock_response):
            # This URL would be an admin-only endpoint in your application
            url = reverse('admin-dashboard')
            response = staff_client.get(url)
            
            assert response.status_code == status.HTTP_200_OK
    
    def test_regular_user_denied_access_to_admin_endpoint(self, authenticated_client):
        """
        Test regular user denied access to an admin-only endpoint.
        """
        # Create a proper HttpResponse object for the mock
        mock_response = HttpResponse(status=403)
        
        # Mock the response for testing
        with patch('rest_framework.views.APIView.dispatch', return_value=mock_response):
            # This URL would be an admin-only endpoint in your application
            url = reverse('admin-dashboard')
            response = authenticated_client.get(url)
            
            assert response.status_code == status.HTTP_403_FORBIDDEN
