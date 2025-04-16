from django.urls import path
from . import views
from . import views_reports
from . import views_search

app_name = 'application'

urlpatterns = [
    # Core application endpoints
    path('applications/', views.ApplicationListView.as_view(), name='application-list'),
    path('applications/<int:pk>/', views.ApplicationDetailView.as_view(), name='application-detail'),
    path('applications/<int:pk>/documents/', views.ApplicationDocumentView.as_view(), name='application-documents'),
    path('applications/<int:pk>/generate-documents/', views.GenerateDocumentView.as_view(), name='generate-documents'),
    path('applications/<int:pk>/notes/', views.NoteCreateView.as_view(), name='create-note'),
    path('applications/<int:pk>/calculator/', views.LoanCalculatorView.as_view(), name='loan-calculator'),
    path('applications/<int:pk>/repayments/', views.RepaymentCreateView.as_view(), name='create-repayment'),
    path('applications/<int:pk>/extension/', views.ExtensionCreateView.as_view(), name='create-extension'),
    path('applications/<int:pk>/duplicate/', views.ApplicationDuplicateView.as_view(), name='duplicate-application'),
    
    # Fee management endpoints
    path('applications/<int:pk>/fees/', views.FeeListView.as_view(), name='application-fees'),
    path('applications/<int:pk>/fees/<int:fee_id>/', views.FeeDetailView.as_view(), name='fee-detail'),
    path('applications/<int:pk>/payments/', views.PaymentListView.as_view(), name='application-payments'),
    path('applications/<int:pk>/payments/<int:payment_id>/', views.PaymentDetailView.as_view(), name='payment-detail'),
    
    # Reporting endpoints
    path('reports/statistics/', views_reports.ApplicationStatisticsView.as_view(), name='application-statistics'),
    path('reports/performance/', views_reports.ApplicationPerformanceView.as_view(), name='application-performance'),
    path('reports/repayments/', views_reports.RepaymentReportView.as_view(), name='repayment-report'),
    
    # Bulk operations
    path('bulk-update/', views_reports.BulkApplicationUpdateView.as_view(), name='bulk-update'),
    
    # Search endpoints
    path('search/advanced/', views_search.AdvancedSearchView.as_view(), name='advanced-search'),
    path('search/global/', views_search.GlobalSearchView.as_view(), name='global-search'),
]
