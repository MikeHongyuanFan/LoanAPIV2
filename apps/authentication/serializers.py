from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile information
    """
    class Meta:
        model = UserProfile
        fields = ['role', 'phone', 'created_at', 'broker', 'borrower']
        read_only_fields = ['created_at']

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user information
    """
    profile = UserProfileSerializer(required=False)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile', 'is_active']
        read_only_fields = ['id', 'is_active']

class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    
    def validate_new_password(self, value):
        validate_password(value)
        return value

class ForgotPasswordSerializer(serializers.Serializer):
    """
    Serializer for password reset request
    """
    email = serializers.EmailField(required=True)

class CreateAccountSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new user account
    """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    role = serializers.ChoiceField(choices=UserProfile.ROLE_CHOICES, required=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    broker_id = serializers.UUIDField(required=False, allow_null=True)
    borrower_id = serializers.UUIDField(required=False, allow_null=True)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email', 'first_name', 'last_name', 'role', 'phone', 'broker_id', 'borrower_id']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        # Check for role-specific validations
        role = attrs.get('role')
        broker_id = attrs.get('broker_id')
        borrower_id = attrs.get('borrower_id')
        
        if role == 'BROKER' and not broker_id:
            raise serializers.ValidationError({"broker_id": "Broker ID is required for broker role."})
        
        if role == 'CLIENT' and not borrower_id:
            raise serializers.ValidationError({"borrower_id": "Borrower ID is required for client role."})
            
        return attrs
