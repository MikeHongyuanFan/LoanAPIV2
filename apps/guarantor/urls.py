from django.urls import path
from . import views

app_name = 'guarantor'

urlpatterns = [
    path('', views.GuarantorCreateView.as_view(), name='guarantor-create'),
    path('<uuid:pk>/', views.GuarantorDetailView.as_view(), name='guarantor-detail'),
]
