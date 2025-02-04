from django.urls import path
from . import views

app_name = 'document_management'

urlpatterns = [
    path('upload/', views.upload_document, name='upload_document'),
    path('list/', views.document_list, name='document_list'),
    path('google-auth/', views.google_auth, name='google_auth'),
    path('google-auth-callback/', views.google_auth_callback, name='google_auth_callback'),
    path('share/<int:document_id>/', views.share_document, name='share_document'),
]