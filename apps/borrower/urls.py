from django.urls import path
from . import views

app_name = 'borrower'

urlpatterns = [
    # Borrower endpoints
    path('borrowers/', views.BorrowerListView.as_view(), name='borrower-list'),
    path('borrowers/<int:pk>/', views.BorrowerDetailView.as_view(), name='borrower-detail'),
    path('borrowers/search/', views.BorrowerSearchView.as_view(), name='borrower-search'),
    path('borrowers/<int:pk>/applications/', views.BorrowerApplicationsView.as_view(), name='borrower-applications'),
    
    # Duplicate detection and merging endpoints
    path('borrowers/check-duplicates/', views.BorrowerDuplicateCheckView.as_view(), name='borrower-check-duplicates'),
    path('borrowers/merge/', views.BorrowerMergeView.as_view(), name='borrower-merge'),
    path('borrowers/merge-history/', views.BorrowerMergeHistoryView.as_view(), name='borrower-merge-history'),
]
