from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ApplicationViewSet, NoteViewSet, RepaymentViewSet, ExtensionViewSet, FeeViewSet

router = DefaultRouter()
router.register(r'applications', ApplicationViewSet)
router.register(r'notes', NoteViewSet)
router.register(r'repayments', RepaymentViewSet)
router.register(r'extensions', ExtensionViewSet)
router.register(r'fees', FeeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
