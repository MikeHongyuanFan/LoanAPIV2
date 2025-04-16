from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

app_name = 'authentication'

urlpatterns = [
    # Authentication endpoints
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('auth/forgot-password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('auth/create-account/', views.CreateAccountView.as_view(), name='create_account'),
    path('auth/delete-account/<int:pk>/', views.DeleteAccountView.as_view(), name='delete_account'),
    
    # User profile endpoints
    path('users/', views.UserProfileListView.as_view(), name='user_list'),
    path('users/<int:pk>/', views.UserProfileDetailView.as_view(), name='user_detail'),
    
    # Permission management endpoints
    path('permissions/', views.PermissionListView.as_view(), name='permission_list'),
    path('permissions/<int:pk>/', views.PermissionDetailView.as_view(), name='permission_detail'),
    path('roles/', views.RoleListView.as_view(), name='role_list'),
    path('roles/<int:pk>/', views.RoleDetailView.as_view(), name='role_detail'),
    path('user-permissions/', views.UserPermissionListView.as_view(), name='user_permission_list'),
    path('user-permissions/<int:pk>/', views.UserPermissionDetailView.as_view(), name='user_permission_detail'),
    
    # Audit log endpoints
    path('audit-logs/', views.AuditLogListView.as_view(), name='audit_log_list'),
]
