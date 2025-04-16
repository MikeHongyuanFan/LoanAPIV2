from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product-list'),
    path('<uuid:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('<uuid:pk>/documents/', views.ProductDocumentsView.as_view(), name='product-documents'),
]
