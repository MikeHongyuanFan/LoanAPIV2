from django.urls import path
from . import views

app_name = 'notification'

urlpatterns = [
    path('', views.NotificationListView.as_view(), name='notification-list'),
    path('<uuid:pk>/', views.NotificationDetailView.as_view(), name='notification-detail'),
    path('settings/', views.NotificationSettingsView.as_view(), name='notification-settings'),
]
