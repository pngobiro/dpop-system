from django.urls import path
from . import views

app_name = 'tasks' # Namespace for the tasks app

urlpatterns = [
    # Department-specific project list (Dashboard)
    path('department/<int:department_id>/projects/', views.department_task_project_list, name='department_task_project_list'),

    # All projects list (Optional)
    path('', views.project_list, name='project_list'),

    # Project URLs
    path('project/<int:project_id>/', views.project_detail, name='project_detail'), # Handles view and attachment POST
    path('project/<int:project_id>/add_task/', views.add_task, name='add_task'),
    # Removed add_project_attachment URL

    # Task URLs
    path('task/<int:task_id>/', views.task_detail, name='task_detail'), # Handles view, comment POST, and attachment POST
    path('task/<int:task_id>/edit/', views.edit_task, name='edit_task'),
    # Removed add_attachment URL

]