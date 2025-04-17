"""
URL Configuration for loan_project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# API Documentation
schema_view = get_schema_view(
   openapi.Info(
      title="Loan Application API",
      default_version='v1',
      description="API for Loan Application System",
      terms_of_service="https://www.example.com/terms/",
      contact=openapi.Contact(email="contact@example.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # API endpoints
    path('api/auth/', include('apps.authentication.urls')),
    path('api/applications/', include('apps.application.urls')),
    path('api/borrowers/', include('apps.borrower.urls')),
    path('api/guarantors/', include('apps.guarantor.urls')),
    path('api/brokers/', include('apps.broker.urls')),
    path('api/valuers/', include('apps.valuer.urls')),
    path('api/qs/', include('apps.qs.urls')),
    path('api/products/', include('apps.product.urls')),
    path('api/documents/', include('apps.document.urls')),
    path('api/notifications/', include('apps.notification.urls')),
    
    # Dashboard
    path('dashboard/', include('apps.dashboard.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
