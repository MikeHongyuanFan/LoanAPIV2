from django.urls import path
from . import views

app_name = 'broker'

urlpatterns = [
    # Broker endpoints
    path('brokers/', views.BrokerListView.as_view(), name='broker-list'),
    path('brokers/<int:pk>/', views.BrokerDetailView.as_view(), name='broker-detail'),
    path('brokers/<int:pk>/applications/', views.BrokerApplicationsView.as_view(), name='broker-applications'),
    path('brokers/<int:pk>/borrowers/', views.BrokerBorrowersView.as_view(), name='broker-borrowers'),
    
    # Commission endpoints
    path('brokers/<int:pk>/commissions/', views.BrokerCommissionsView.as_view(), name='broker-commissions'),
    path('brokers/<int:pk>/commission-summary/', views.BrokerCommissionSummaryView.as_view(), name='broker-commission-summary'),
    path('commissions/', views.BrokerCommissionListView.as_view(), name='commission-list'),
    path('commissions/<int:pk>/', views.BrokerCommissionDetailView.as_view(), name='commission-detail'),
    
    # Commission payment endpoints
    path('commission-payments/', views.CommissionPaymentListView.as_view(), name='commission-payment-list'),
    path('commission-payments/<int:pk>/', views.CommissionPaymentDetailView.as_view(), name='commission-payment-detail'),
]
