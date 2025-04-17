from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import UserProfile
from .permissions import IsStaff


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint for user profiles.
    """
    queryset = UserProfile.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def retrieve_own(self, request):
        """
        Retrieve the current user's profile.
        """
        user_profile = request.user.profile
        # Serialize the user profile
        data = {
            'id': user_profile.id,
            'username': request.user.username,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'phone': user_profile.phone,
            'position': user_profile.position,
            'department': user_profile.department,
            'is_staff': request.user.is_staff,
            'is_superuser': request.user.is_superuser,
        }
        return Response(data)


class AdminDashboardView(APIView):
    """
    API endpoint for admin dashboard.
    """
    permission_classes = [IsStaff]
    
    def get(self, request):
        """
        Get admin dashboard data.
        """
        # This would be implemented with actual dashboard data
        data = {
            'message': 'Admin dashboard data',
            'user_count': User.objects.count(),
        }
        return Response(data)
