from django.urls import path
from . import views

urlpatterns = [
    path('', views.BorrowerListCreateView.as_view(), name='borrower-list'),
    path('<int:pk>/', views.BorrowerDetailView.as_view(), name='borrower-detail'),
    path('search/', views.BorrowerSearchView.as_view(), name='borrower-search'),
    path('merge/', views.BorrowerMergeView.as_view(), name='borrower-merge'),
    path('check-duplicates/', views.BorrowerCheckDuplicatesView.as_view(), name='borrower-check-duplicates'),
    path('merge-history/', views.BorrowerMergeHistoryView.as_view(), name='borrower-merge-history'),
]
