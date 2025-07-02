"""
Task listing views for viewing assigned and created tasks.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from authentication.models import CustomUser
from apps.tasks.models import Task, Project
from apps.meetings.models import Meeting
from apps.tasks.utils.statistics import get_task_statistics


@login_required
def tasks_assigned_by_me(request):
    """View for tasks that are assigned to the current user"""
    # Retrieve tasks assigned to the current user
    tasks_assigned_to_me_queryset = Task.objects.filter(
        assignees=request.user
    ).select_related(
        'project'
    ).prefetch_related(
        'assignees'
    ).order_by(
        'status',  # Order by status first
        '-due_date',  # Then by due date (most recent first)
        '-created_at'  # Then by creation date
    )

    # Calculate statistics using the helper function
    assigned_tasks_stats = get_task_statistics(tasks_assigned_to_me_queryset)

    # Retrieve all active users for the assign task modal (excluding current user)
    users = CustomUser.objects.filter(is_active=True).exclude(id=request.user.id)
    projects = Project.objects.all()
    meetings = Meeting.objects.all() # Fetch all meetings

    context = {
        'tasks': tasks_assigned_to_me_queryset, # Pass tasks assigned to the user
        'title': 'Tasks Assigned to Me', # Page title
        'users': users,
        'projects': projects,
        'meetings': meetings, # Pass meetings to the template
        'request': request,
        'assigned_tasks_stats': assigned_tasks_stats, # Pass the calculated stats
    }
    return render(request, 'tasks/tasks_assigned.html', context)


@login_required
def tasks_created_by_me(request):
    """View for tasks that the user has created"""
    # Retrieve tasks created by the current user
    tasks_created_by_me_queryset = Task.objects.filter(
        creator=request.user
    ).select_related(
        'project'
    ).prefetch_related(
        'assignees'
    ).order_by(
        'status',  # Order by status first
        '-due_date',  # Then by due date (most recent first)
        '-created_at'  # Then by creation date
    )

    # Calculate statistics using the helper function
    created_tasks_stats = get_task_statistics(tasks_created_by_me_queryset)

    # Retrieve all active users for the assign task modal (excluding current user)
    users = CustomUser.objects.filter(is_active=True).exclude(id=request.user.id)
    projects = Project.objects.all()

    context = {
        'tasks': tasks_created_by_me_queryset, # Pass tasks created by the user
        'title': 'Tasks I Assigned', # Page title
        'users': users,
        'projects': projects,
        'request': request,
        'assigned_tasks_stats': created_tasks_stats, # Pass the calculated stats (using assigned_tasks_stats key for template compatibility)
    }
    return render(request, 'tasks/tasks_assigned.html', context)
