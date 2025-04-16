from django.urls import path
from . import views

app_name = 'application'

urlpatterns = [
    path('', views.ApplicationListView.as_view(), name='application-list'),
    path('<uuid:pk>/', views.ApplicationDetailView.as_view(), name='application-detail'),
    path('<uuid:pk>/documents/', views.ApplicationDocumentView.as_view(), name='application-documents'),
    path('<uuid:pk>/generate-documents/', views.GenerateDocumentView.as_view(), name='generate-documents'),
    path('<uuid:pk>/notes/', views.NoteCreateView.as_view(), name='create-note'),
    path('<uuid:pk>/calculator/', views.LoanCalculatorView.as_view(), name='loan-calculator'),
    path('<uuid:pk>/repayments/', views.RepaymentCreateView.as_view(), name='create-repayment'),
    path('<uuid:pk>/extension/', views.ExtensionCreateView.as_view(), name='create-extension'),
    path('<uuid:pk>/fees/', views.FeeListCreateView.as_view(), name='fee-list'),
    path('<uuid:application_pk>/fees/<uuid:pk>/', views.FeeDetailView.as_view(), name='fee-detail'),
    path('<uuid:pk>/payments/', views.PaymentListCreateView.as_view(), name='payment-list'),
    path('<uuid:application_pk>/payments/<uuid:pk>/', views.PaymentDetailView.as_view(), name='payment-detail'),
    path('<uuid:pk>/duplicate/', views.ApplicationDuplicateView.as_view(), name='application-duplicate'),
]
