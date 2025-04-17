from django.urls import path
from . import views
from . import views_templates

urlpatterns = [
    path('', views.NotificationListView.as_view(), name='notification-list'),
    path('<int:pk>/', views.NotificationDetailView.as_view(), name='notification-detail'),
    path('settings/', views.NotificationSettingView.as_view(), name='notification-settings'),
    path('templates/', views_templates.NotificationTemplateListView.as_view(), name='notification-template-list'),
    path('templates/<int:pk>/', views_templates.NotificationTemplateDetailView.as_view(), name='notification-template-detail'),
    path('templates/preview/', views_templates.NotificationTemplatePreviewView.as_view(), name='notification-template-preview'),
    path('send-email/', views_templates.SendEmailNotificationView.as_view(), name='send-email-notification'),
]
