from django.urls import path
from . import views

app_name = 'broker'

urlpatterns = [
    path('', views.BrokerListView.as_view(), name='broker-list'),
    path('<uuid:pk>/', views.BrokerDetailView.as_view(), name='broker-detail'),
    path('<uuid:pk>/applications/', views.BrokerApplicationsView.as_view(), name='broker-applications'),
    path('<uuid:pk>/borrowers/', views.BrokerBorrowersView.as_view(), name='broker-borrowers'),
]
