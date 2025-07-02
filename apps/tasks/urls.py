from django.urls import path
from .views.dashboard import user_tasks_dashboard, my_dashboard, tasks_assigned_by_me, assign_task, tasks_created_by_me, DepartmentListView
from .views.projects import ProjectListView, ProjectDetailView, ProjectCreateView, ProjectUpdateView, ProjectDeleteView, DepartmentProjectListView
from .views.tasks import TaskDetailView, TaskCreateView, TaskUpdateView, add_attachment_comment, update_task_status, revert_task_to_history, reassign_task


app_name = 'tasks' # Namespace for the tasks app
urlpatterns = [
    # User dashboard
    path('admin/', user_tasks_dashboard, name='dashboard'),
    path('my_dashboard/', my_dashboard, name='my_dashboard'),
    path('assigned/', tasks_assigned_by_me, name='tasks_assigned_by_me'),
    path('created_by_me/', tasks_created_by_me, name='tasks_created_by_me'),
    path('assign-task/', assign_task, name='assign_task'),
    
    # Department-specific project list
    path('departments/<int:department_id>/projects/', DepartmentProjectListView.as_view(), name='department_project_list'),

    # Project URLs
    path('projects/', ProjectListView.as_view(), name='project_list'),
    path('departments/', DepartmentListView.as_view(), name='department_list'),
    path('projects/create/', ProjectCreateView.as_view(), name='project_create'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('projects/<int:pk>/edit/', ProjectUpdateView.as_view(), name='project_update'),
    path('projects/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete'),

    # Task URLs
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('projects/<int:project_pk>/tasks/create/', TaskCreateView.as_view(), name='task_create'),
    path('tasks/<int:pk>/edit/', TaskUpdateView.as_view(), name='task_update'),

    # Attachment URLs
    path('attachments/<int:attachment_id>/comment/', add_attachment_comment, name='add_attachment_comment'),
    path('tasks/<int:pk>/update_status/', update_task_status, name='update_task_status'),
    path('tasks/<int:pk>/revert/<int:history_id>/', revert_task_to_history, name='revert_task_to_history'),
    path('tasks/<int:pk>/reassign/', reassign_task, name='reassign_task'),
]