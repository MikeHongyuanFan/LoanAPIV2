from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListCreateView.as_view(), name='product-list'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('<int:product_id>/requirements/', views.ProductDocumentRequirementListView.as_view(), name='product-requirements'),
    path('requirements/<int:pk>/', views.ProductDocumentRequirementDetailView.as_view(), name='requirement-detail'),
]
