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
    # Custom endpoints for valuer and QS info
    path('applications/<uuid:pk>/update-valuer-info/', ApplicationViewSet.as_view({'post': 'update_valuer_info'}), name='application-update-valuer-info'),
    path('applications/<uuid:pk>/update-qs-info/', ApplicationViewSet.as_view({'post': 'update_qs_info'}), name='application-update-qs-info'),
]
