from django.urls import path
from . import views

urlpatterns = [
    path('', views.DocumentListView.as_view(), name='document-list'),
    path('<int:pk>/', views.DocumentDetailView.as_view(), name='document-detail'),
    path('upload/', views.UploadDocumentView.as_view(), name='document-upload'),
    path('generate/', views.GenerateDocumentView.as_view(), name='document-generate'),
    path('templates/', views.DocumentTemplateListView.as_view(), name='document-template-list'),
    path('templates/<int:pk>/', views.DocumentTemplateDetailView.as_view(), name='document-template-detail'),
    path('docusign/', views.DocuSignIntegrationView.as_view(), name='docusign-integration'),
    path('send-for-signing/', views.DocumentSendForSigningView.as_view(), name='document-send-for-signing'),
    path('signing-requests/', views.DocumentSigningRequestListView.as_view(), name='signing-request-list'),
    path('signing-requests/<int:pk>/', views.DocumentSigningRequestDetailView.as_view(), name='signing-request-detail'),
    path('application/<int:application_id>/', views.DocumentsByApplicationView.as_view(), name='documents-by-application'),
]
