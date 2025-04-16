from django.urls import path
from . import views
from . import views_templates
from . import views_scheduled

app_name = 'notification'

urlpatterns = [
    # Notification endpoints
    path('notifications/', views.NotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:pk>/', views.NotificationDetailView.as_view(), name='notification-detail'),
    path('notifications/<int:pk>/send/', views.SendNotificationView.as_view(), name='send-notification'),
    
    # Notification settings endpoints
    path('notifications/settings/', views.NotificationSettingsView.as_view(), name='notification-settings'),
    
    # Notification template endpoints
    path('notifications/templates/', views_templates.NotificationTemplateListView.as_view(), name='notification-template-list'),
    path('notifications/templates/<int:pk>/', views_templates.NotificationTemplateDetailView.as_view(), name='notification-template-detail'),
    path('notifications/templates/<int:pk>/preview/', views_templates.NotificationTemplatePreviewView.as_view(), name='notification-template-preview'),
    path('notifications/templates/<int:pk>/send-test/', views_templates.SendTestNotificationView.as_view(), name='send-test-notification'),
    
    # Process pending notifications
    path('notifications/process-pending/', views.ProcessPendingNotificationsView.as_view(), name='process-pending-notifications'),
    
    # SMS notification endpoint
    path('notifications/send-sms/', views_templates.SMSNotificationView.as_view(), name='send-sms'),
    
    # Scheduled notification endpoints
    path('notifications/repayment-reminders/', views_scheduled.RepaymentReminderView.as_view(), name='repayment-reminders'),
    path('notifications/late-repayment-reminders/', views_scheduled.LateRepaymentReminderView.as_view(), name='late-repayment-reminders'),
    path('notifications/loan-expiration-reminders/', views_scheduled.LoanExpirationReminderView.as_view(), name='loan-expiration-reminders'),
    path('notifications/stagnant-stage-reminders/', views_scheduled.StagnantStageReminderView.as_view(), name='stagnant-stage-reminders'),
]
