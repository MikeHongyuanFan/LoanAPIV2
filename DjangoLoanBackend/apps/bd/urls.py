from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BDViewSet

router = DefaultRouter()
router.register(r'bds', BDViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
