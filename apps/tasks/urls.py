from django.urls import path
from django.urls import path
from .views.dashboard import user_tasks_dashboard, my_dashboard, tasks_assigned_by_me, assign_task
from .views.projects import project_list, department_task_project_list, project_detail
from .views.tasks import task_detail, add_task, edit_task


app_name = 'tasks' # Namespace for the tasks app
urlpatterns = [
    # User dashboard
    path('admin/', user_tasks_dashboard, name='dashboard'),
    path('my_dashboard/', my_dashboard, name='my_dashboard'),
    path('assigned/', tasks_assigned_by_me, name='tasks_assigned_by_me'),
    path('assign-task/', assign_task, name='assign_task'),
    
    # Department-specific project list
    path('department/<int:department_id>/projects/', department_task_project_list, name='department_task_project_list'),

    # All projects list
    path('projects/', project_list, name='project_list'),

    # Project URLs

    path('project/<int:project_id>/', project_detail, name='project_detail'), # Handles view and attachment POST
    path('project/<int:project_id>/add_task/', add_task, name='add_task'),
    # Removed add_project_attachment URL

    # Task URLs
    path('task/<int:task_id>/', task_detail, name='task_detail'), # Handles view, comment POST, and attachment POST
    path('task/<int:task_id>/edit/', edit_task, name='edit_task'),
    # Removed add_attachment URL

]