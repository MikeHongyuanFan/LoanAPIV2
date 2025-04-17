from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'brokers', views.BrokerViewSet)
router.register(r'broker-tiers', views.BrokerTierViewSet)
router.register(r'broker-specializations', views.BrokerSpecializationViewSet)
router.register(r'broker-commissions', views.BrokerCommissionViewSet)
router.register(r'commission-payments', views.CommissionPaymentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
