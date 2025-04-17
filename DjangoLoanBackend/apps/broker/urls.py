from django.urls import path
from . import views

urlpatterns = [
    path('', views.BrokerListCreateView.as_view(), name='broker-list'),
    path('<int:pk>/', views.BrokerDetailView.as_view(), name='broker-detail'),
    path('<int:broker_id>/commissions/', views.BrokerCommissionListView.as_view(), name='broker-commissions'),
    path('commissions/<int:pk>/', views.BrokerCommissionDetailView.as_view(), name='commission-detail'),
    path('payments/', views.CommissionPaymentListCreateView.as_view(), name='commission-payments'),
    path('payments/<int:pk>/', views.CommissionPaymentDetailView.as_view(), name='commission-payment-detail'),
]
