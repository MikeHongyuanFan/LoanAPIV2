from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'companies', views.CompanyViewSet)
router.register(r'directors', views.DirectorViewSet)
router.register(r'shareholders', views.ShareholderViewSet)
router.register(r'financials', views.FinancialInformationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
