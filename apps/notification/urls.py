from django.urls import path
from . import views

app_name = 'notification'

urlpatterns = [
    path('', views.NotificationListView.as_view(), name='notification-list'),
    path('<uuid:pk>/', views.NotificationDetailView.as_view(), name='notification-detail'),
    path('<uuid:pk>/send/', views.NotificationSendView.as_view(), name='notification-send'),
    path('settings/', views.NotificationSettingsUpdateView.as_view(), name='notification-settings'),
    path('settings/list/', views.NotificationSettingListView.as_view(), name='notification-setting-list'),
    path('settings/<uuid:pk>/', views.NotificationSettingDetailView.as_view(), name='notification-setting-detail'),
    path('templates/', views.NotificationTemplateListView.as_view(), name='notification-template-list'),
    path('templates/<uuid:pk>/', views.NotificationTemplateDetailView.as_view(), name='notification-template-detail'),
    path('process-pending/', views.PendingNotificationsView.as_view(), name='process-pending-notifications'),
]
