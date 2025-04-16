from django.urls import path
from . import views

app_name = 'document'

urlpatterns = [
    path('generate/', views.GenerateDocumentView.as_view(), name='generate-document'),
    path('<uuid:pk>/', views.DocumentDetailView.as_view(), name='document-detail'),
    path('upload/', views.UploadDocumentView.as_view(), name='upload-document'),
]
