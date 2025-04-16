from django.urls import path
from . import views

app_name = 'borrower'

urlpatterns = [
    path('', views.BorrowerListView.as_view(), name='borrower-list'),
    path('<uuid:pk>/', views.BorrowerDetailView.as_view(), name='borrower-detail'),
    path('search/', views.BorrowerSearchView.as_view(), name='borrower-search'),
    path('<uuid:pk>/applications/', views.BorrowerApplicationsView.as_view(), name='borrower-applications'),
]
