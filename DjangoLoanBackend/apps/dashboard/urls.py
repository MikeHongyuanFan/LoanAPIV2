from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Dashboard endpoints
    path('dashboard/summary/', views.DashboardSummaryView.as_view(), name='dashboard-summary'),
    path('dashboard/user/', views.UserDashboardView.as_view(), name='user-dashboard'),
    path('dashboard/manager/', views.ManagerDashboardView.as_view(), name='manager-dashboard'),
]
