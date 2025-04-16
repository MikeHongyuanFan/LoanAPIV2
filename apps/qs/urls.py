from django.urls import path
from . import views

app_name = 'qs'

urlpatterns = [
    path('', views.QSListView.as_view(), name='qs-list'),
    path('<uuid:pk>/', views.QSDetailView.as_view(), name='qs-detail'),
    path('<uuid:pk>/applications/', views.QSApplicationsView.as_view(), name='qs-applications'),
]
