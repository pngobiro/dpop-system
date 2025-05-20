from .dashboard import user_tasks_dashboard
from .projects import (
    project_list,
    department_task_project_list,
    project_detail
)
from .tasks import (
    task_detail,
    add_task,
    edit_task
)

__all__ = [
    'user_tasks_dashboard',
    'project_list',
    'department_task_project_list',
    'project_detail',
    'task_detail',
    'add_task',
    'edit_task'
]