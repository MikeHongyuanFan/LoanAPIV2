from django.urls import path
from . import views

app_name = 'valuer'

urlpatterns = [
    path('', views.ValuerListView.as_view(), name='valuer-list'),
    path('<uuid:pk>/', views.ValuerDetailView.as_view(), name='valuer-detail'),
    path('<uuid:pk>/applications/', views.ValuerApplicationsView.as_view(), name='valuer-applications'),
]
