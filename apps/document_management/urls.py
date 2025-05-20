from django.urls import path
from .views.drive_views import (
    google_drive_files,
    import_drive_file,
    share_drive_file,
    summarize_document
)

app_name = 'apps.document_management'

urlpatterns = [
    # Main URL redirecting to Google Drive
    path('library/', google_drive_files, name='library'),
    
    # Google Drive URLs
    path('drive/files/', google_drive_files, name='drive_files'),
    path('drive/files/<str:folder_id>/', google_drive_files, name='drive_files'),
    path('drive/import/<str:file_id>/', import_drive_file, name='import_drive_file'),
    path('drive/share/<int:document_id>/', share_drive_file, name='share_drive_file'),
    path('drive/summarize/<str:file_id>/', summarize_document, name='summarize_document'),
]