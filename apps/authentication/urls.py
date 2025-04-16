from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'authentication'

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot-password'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('create-account/', views.CreateAccountView.as_view(), name='create-account'),
    path('delete-account/', views.DeleteAccountView.as_view(), name='delete-account'),
]
