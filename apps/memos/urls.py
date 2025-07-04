# apps/memos/urls.py
from django.urls import path
from . import views

app_name = 'memos'

urlpatterns = [
    # Dashboard
    path('', views.department_dashboard, name='department_dashboard'),
    path('my-memos/', views.my_memos, name='my_memos'),
    
    # Memo CRUD
    path('create/', views.memo_create, name='memo_create'),
    path('<uuid:pk>/', views.memo_detail, name='memo_detail'),
    path('<uuid:pk>/edit/', views.memo_edit, name='memo_edit'),
    path('<uuid:pk>/delete/', views.memo_delete, name='memo_delete'),

    # Related Actions
    path('<uuid:pk>/create-task/', views.create_task_from_memo, name='create_task_from_memo'),
    path('<uuid:pk>/create-meeting/', views.create_meeting_from_memo, name='create_meeting_from_memo'),
    
    # Workflow and Status
    path('<uuid:pk>/status-update/', views.memo_status_update, name='memo_status_update'),
    
    # Comments
    path('<uuid:pk>/comment/', views.add_comment, name='add_comment'),
    
    # API endpoints for AJAX
    path('api/memo/<uuid:pk>/attachments/', views.memo_attachments, name='memo_attachments'),
]