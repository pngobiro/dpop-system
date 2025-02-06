# apps/memos/urls.py
from django.urls import path
from . import views

app_name = 'apps.memos'

urlpatterns = [
    # Dashboard
    path('', views.department_dashboard, name='department_dashboard'),
    path('my-memos/', views.my_memos, name='my_memos'),
    path('pending-approvals/', views.pending_approvals, name='pending_approvals'),
    
    # Memo CRUD
    path('create/', views.memo_create, name='memo_create'),
    path('<int:pk>/', views.memo_detail, name='memo_detail'),
    path('<int:pk>/edit/', views.memo_edit, name='memo_edit'),
    path('<int:pk>/delete/', views.memo_delete, name='memo_delete'),
    
    # Workflow
    path('<int:pk>/submit/', views.memo_submit, name='memo_submit'),
    path('<int:pk>/approve/', views.memo_approve, name='memo_approve'),
    path('<int:pk>/reject/', views.memo_reject, name='memo_reject'),
    path('<int:pk>/publish/', views.memo_publish, name='memo_publish'),
    
    # Comments
    path('<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:pk>/reply/', views.add_reply, name='add_reply'),
    
    # Templates
    path('templates/', views.template_list, name='template_list'),
    path('templates/create/', views.template_create, name='template_create'),
    path('templates/<int:pk>/edit/', views.template_edit, name='template_edit'),
    
    # API endpoints for AJAX
    path('api/memo/<int:pk>/status/', views.memo_status_update, name='memo_status_update'),
    path('api/memo/<int:pk>/attachments/', views.memo_attachments, name='memo_attachments'),
]