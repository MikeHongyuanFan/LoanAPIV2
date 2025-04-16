from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings

from .models import UserProfile, Permission, Role, UserPermission, AuditLog
from .serializers import (
    UserProfileSerializer, UserCreateSerializer, ChangePasswordSerializer,
    ForgotPasswordSerializer, PermissionSerializer, RoleSerializer,
    UserPermissionSerializer, AuditLogSerializer
)
from .permissions import IsAdmin, IsManager


class UserProfileListView(generics.ListAPIView):
    """
    API endpoint for listing user profiles.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsManager]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['role', 'department']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name']


class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for retrieving and updating a user profile.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsManager]
    
    def get_object(self):
        """
        Users can view their own profile, managers can view any profile.
        """
        if self.request.user.profile.role in ['ADMIN', 'MANAGER']:
            return super().get_object()
        return self.request.user.profile


class CreateAccountView(generics.CreateAPIView):
    """
    API endpoint for creating a new user account.
    """
    serializer_class = UserCreateSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


class ChangePasswordView(APIView):
    """
    API endpoint for changing user password.
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):
    """
    API endpoint for requesting a password reset.
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            
            # Generate password reset token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Send password reset email
            reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
            send_mail(
                subject="Password Reset Request",
                message=f"Please click the link below to reset your password:\n\n{reset_url}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            
            return Response({"message": "Password reset email sent."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteAccountView(APIView):
    """
    API endpoint for deactivating a user account.
    """
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            # Deactivate instead of delete
            user.is_active = False
            user.save()
            return Response({"message": "User account deactivated successfully."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)


class PermissionListView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating permissions.
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['resource', 'action']


class PermissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting a permission.
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


class RoleListView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating roles.
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


class RoleDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting a role.
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


class UserPermissionListView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating user permissions.
    """
    serializer_class = UserPermissionSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'permission', 'granted']
    
    def get_queryset(self):
        return UserPermission.objects.all()


class UserPermissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting a user permission.
    """
    queryset = UserPermission.objects.all()
    serializer_class = UserPermissionSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


class AuditLogListView(generics.ListAPIView):
    """
    API endpoint for listing audit logs.
    """
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['user', 'action', 'resource_type', 'timestamp']
    search_fields = ['user__user__username', 'resource_id', 'ip_address']
    
    def get_queryset(self):
        return AuditLog.objects.all().order_by('-timestamp')
