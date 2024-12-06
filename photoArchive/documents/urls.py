from django.urls import path
from .views import DocumentDetailView, DocumentUpdateView, DocumentDeleteView, document_search, document_create_view

urlpatterns = [
    path('', document_search, name='document_search'),
    path('<int:pk>', DocumentDetailView.as_view(), name='document_detail'),
    path('new', document_create_view, name='document_create'),
    path('<int:pk>/edit', DocumentUpdateView.as_view(), name='document_update'),
    path('<int:pk>/delete', DocumentDeleteView.as_view(), name='document_delete'),
]
