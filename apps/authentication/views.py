from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db import transaction

from .models import UserProfile
from .serializers import (
    UserSerializer, 
    ChangePasswordSerializer, 
    ForgotPasswordSerializer,
    CreateAccountSerializer
)
from apps.broker.models import Broker
from apps.borrower.models import Borrower

class ChangePasswordView(APIView):
    """
    Change user password
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            user = request.user
            
            # Check if old password is correct
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            
            # Set new password
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            return Response({
                "message": "Password changed successfully"
            }, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(APIView):
    """
    Request password reset
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            # Check if user exists
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                # Don't reveal that the user doesn't exist
                return Response({
                    "message": "If your email is registered, you will receive a password reset link."
                }, status=status.HTTP_200_OK)
            
            # In a real implementation, this would generate a token and send an email
            # For now, we'll just return a success message
            
            return Response({
                "message": "If your email is registered, you will receive a password reset link."
            }, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateAccountView(APIView):
    """
    Create a new user account
    """
    permission_classes = [IsAuthenticated]
    
    @transaction.atomic
    def post(self, request):
        # Only admins and managers can create accounts
        if not request.user.profile.role in ['ADMIN', 'MANAGER']:
            return Response({
                "message": "You don't have permission to create accounts"
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = CreateAccountSerializer(data=request.data)
        
        if serializer.is_valid():
            # Extract profile-related data
            role = serializer.validated_data.pop('role')
            phone = serializer.validated_data.pop('phone', '')
            broker_id = serializer.validated_data.pop('broker_id', None)
            borrower_id = serializer.validated_data.pop('borrower_id', None)
            password = serializer.validated_data.pop('password')
            serializer.validated_data.pop('password2')
            
            # Create user
            user = User.objects.create_user(
                **serializer.validated_data,
                password=password
            )
            
            # Get related objects if needed
            broker = None
            if broker_id:
                broker = get_object_or_404(Broker, id=broker_id)
                
            borrower = None
            if borrower_id:
                borrower = get_object_or_404(Borrower, id=borrower_id)
            
            # Create profile
            UserProfile.objects.create(
                user=user,
                role=role,
                phone=phone,
                broker=broker,
                borrower=borrower
            )
            
            return Response({
                "message": "User account created successfully",
                "user_id": user.id
            }, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteAccountView(APIView):
    """
    Delete a user account
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Only admins can delete accounts
        if not request.user.profile.role == 'ADMIN':
            return Response({
                "message": "You don't have permission to delete accounts"
            }, status=status.HTTP_403_FORBIDDEN)
        
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({
                "message": "User ID is required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
            
            # Don't allow deleting your own account
            if user == request.user:
                return Response({
                    "message": "You cannot delete your own account"
                }, status=status.HTTP_400_BAD_REQUEST)
                
            # Soft delete by deactivating
            user.is_active = False
            user.save()
            
            return Response({
                "message": "User account deactivated successfully"
            }, status=status.HTTP_200_OK)
            
        except User.DoesNotExist:
            return Response({
                "message": "User not found"
            }, status=status.HTTP_404_NOT_FOUND)
