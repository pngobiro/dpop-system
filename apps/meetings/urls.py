# apps/meetings/urls.py
from django.urls import path
from . import views

app_name = 'meetings'

urlpatterns = [
    path('', views.meetings_dashboard, name='dashboard'),  # Add this line at the top
    path('list/', views.meeting_list, name='meeting_list'),
    path('create/', views.meeting_create, name='meeting_create'),
    path('<int:pk>/', views.meeting_detail, name='meeting_detail'),
    path('<int:pk>/edit/', views.meeting_update, name='meeting_update'),
    path('<int:pk>/delete/', views.meeting_delete, name='meeting_delete'),
    path('<int:meeting_pk>/documents/upload/', 
         views.meeting_document_upload, name='meeting_document_upload'),
    path('<int:meeting_pk>/action/create/', 
         views.action_item_create, name='action_item_create'),
]