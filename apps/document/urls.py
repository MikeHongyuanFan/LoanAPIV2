from django.urls import path
from . import views

app_name = 'document'

urlpatterns = [
    path('generate/', views.GenerateDocumentView.as_view(), name='generate-document'),
    path('<uuid:pk>/', views.DocumentDetailView.as_view(), name='document-detail'),
    path('upload/', views.UploadDocumentView.as_view(), name='upload-document'),
    path('templates/', views.DocumentTemplateListView.as_view(), name='template-list'),
    path('templates/<uuid:pk>/', views.DocumentTemplateDetailView.as_view(), name='template-detail'),
    path('docusign/', views.DocuSignIntegrationView.as_view(), name='docusign-integration'),
    path('send-for-signing/', views.DocumentSendForSigningView.as_view(), name='send-for-signing'),
    path('signing-requests/', views.DocumentSigningRequestListView.as_view(), name='signing-request-list'),
    path('signing-requests/<uuid:pk>/', views.DocumentSigningRequestDetailView.as_view(), name='signing-request-detail'),
    path('application/<uuid:application_id>/', views.DocumentsByApplicationView.as_view(), name='documents-by-application'),
]
