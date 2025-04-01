from django.urls import path
from . import views

app_name = 'document_management'

urlpatterns = [
    path('library/', views.digital_library, name='digital_library'),
    path('document/<int:doc_id>/', views.document_detail, name='document_detail'),
    path('document/<int:doc_id>/summarize/', views.summarize_document, name='summarize_document'),
    path('document/<int:doc_id>/download/', views.download_document, name='download_document'),
    path('document/<int:doc_id>/share/', views.share_document, name='share_document'),
]