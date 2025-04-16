from django.urls import path
from . import views
from . import views_docusign

app_name = 'document'

urlpatterns = [
    # Document management endpoints
    path('documents/generate/', views.GenerateDocumentView.as_view(), name='generate-document'),
    path('documents/<int:pk>/', views.DocumentDetailView.as_view(), name='document-detail'),
    path('documents/upload/', views.UploadDocumentView.as_view(), name='upload-document'),
    
    # Document template endpoints
    path('documents/templates/', views.DocumentTemplateListView.as_view(), name='document-template-list'),
    path('documents/templates/<int:pk>/', views.DocumentTemplateDetailView.as_view(), name='document-template-detail'),
    
    # Document signing endpoints
    path('documents/send-for-signing/', views.SendForSigningView.as_view(), name='send-for-signing'),
    path('documents/signing-requests/', views.SigningRequestListView.as_view(), name='signing-request-list'),
    path('documents/signing-requests/<int:pk>/', views.SigningRequestDetailView.as_view(), name='signing-request-detail'),
    
    # DocuSign integration endpoints
    path('documents/docusign-callback/', views_docusign.DocuSignCallbackView.as_view(), name='docusign-callback'),
    
    # Document version control endpoints
    path('documents/<int:document_id>/versions/', views_docusign.DocumentVersionView.as_view(), name='document-versions'),
]
